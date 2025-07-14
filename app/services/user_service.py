from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
from passlib.context import CryptContext
from pymongo import ReturnDocument

from app.core.config import settings
from app.schemas.user import UserCreate, FoodPreferences, PlayPreferences, UserUpdate
from app.models.user import UserModel
from app.models.group import GroupModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client[settings.MONGO_DATABASE]
        self.collection = self.db.users
        self.group_collection = self.db.groups

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def get_user(self, user_id: str) -> Optional[UserModel]:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return UserModel(**user)
        return None

    async def get_user_by_userid(self, userid: str) -> Optional[UserModel]:
        user = await self.collection.find_one({"userid": userid})
        if user:
            return UserModel(**user)
        return None

    async def create_user(self, user_in: UserCreate) -> UserModel:
        hashed_password = self.get_password_hash(user_in.password)
        user_dict = user_in.dict()
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]

        user_dict.update({
            "food_preferences": FoodPreferences().dict(),
            "play_preferences": PlayPreferences().dict(),
            "activity_log": []
        })
        
        new_user = await self.collection.insert_one(user_dict)
        created_user = await self.collection.find_one({"_id": new_user.inserted_id})
        
        return UserModel(**created_user)

    async def update_user(self, user_id: str, user_in: UserUpdate) -> Optional[UserModel]:
        update_data = user_in.dict(exclude_unset=True)

        if "food_preferences" in update_data:
            update_data["food_preferences"] = update_data["food_preferences"]
        if "play_preferences" in update_data:
            update_data["play_preferences"] = update_data["play_preferences"]

        if not update_data:
            return await self.get_user(user_id)

        updated_user = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

        if updated_user:
            if "food_preferences" in update_data or "play_preferences" in update_data:
                user_model = UserModel(**updated_user)
                if user_model.group_ids:
                    from app.services.group_service import GroupService
                    group_service = GroupService(self.db.client)
                    for group_id in user_model.group_ids:
                        await group_service.calculate_and_update_group_preferences(group_id)
            
            return UserModel(**updated_user)
        return None

    async def add_group_to_user(self, user_id: str, group_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"group_ids": group_id}}
        )
        return result.modified_count > 0

    async def remove_group_from_user(self, user_id: str, group_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"group_ids": group_id}}
        )
        return result.modified_count > 0

    async def remove_group_from_all_users(self, user_ids: List[str], group_id: str) -> bool:
        result = await self.collection.update_many(
            {"_id": {"$in": [ObjectId(uid) for uid in user_ids]}},
            {"$pull": {"group_ids": group_id}}
        )
        return result.modified_count > 0

    async def get_user_groups(self, user: UserModel) -> List[dict]:
        group_ids_as_obj = [ObjectId(gid) for gid in user.group_ids]
        
        pipeline = [
            {"$match": {"_id": {"$in": group_ids_as_obj}}},
            {"$addFields": {
                "member_oids": {
                    "$map": {
                        "input": "$member_ids",
                        "as": "member_id_str",
                        "in": {"$toObjectId": "$$member_id_str"}
                    }
                }
            }},
            {"$lookup": {
                "from": "users",
                "localField": "member_oids",
                "foreignField": "_id",
                "as": "member_details"
            }},
            {"$project": {
                "id": {"$toString": "$_id"},
                "groupname": 1,
                "starttime": 1,
                "endtime": 1,
                "is_active": 1,
                "owner_id": 1,
                "food_preferences": 1,
                "play_preferences": 1,
                "members": {
                    "$map": {
                        "input": "$member_details",
                        "as": "member",
                        "in": {
                            "id": {"$toString": "$$member._id"},
                            "name": "$$member.username"
                        }
                    }
                }
            }}
        ]
        
        groups_cursor = self.group_collection.aggregate(pipeline)
        groups = await groups_cursor.to_list(length=None)
        return groups

    async def get_user_group_by_id(self, user: UserModel, group_id: str) -> Optional[dict]:
        if group_id not in user.group_ids:
            return None

        group_obj_id = ObjectId(group_id)
        
        pipeline = [
            {"$match": {"_id": group_obj_id}},
            {"$addFields": {
                "member_oids": {
                    "$map": {
                        "input": "$member_ids",
                        "as": "member_id_str",
                        "in": {"$toObjectId": "$$member_id_str"}
                    }
                }
            }},
            {"$lookup": {
                "from": "users",
                "localField": "member_oids",
                "foreignField": "_id",
                "as": "member_details"
            }},
            {"$project": {
                "id": {"$toString": "$_id"},
                "groupname": 1,
                "starttime": 1,
                "endtime": 1,
                "is_active": 1,
                "owner_id": 1,
                "food_preferences": 1,
                "play_preferences": 1,
                "members": {
                    "$map": {
                        "input": "$member_details",
                        "as": "member",
                        "in": {
                            "id": {"$toString": "$$member._id"},
                            "name": "$$member.username"
                        }
                    }
                }
            }}
        ]
        
        groups_cursor = self.group_collection.aggregate(pipeline)
        group = await groups_cursor.to_list(length=1)
        return group[0] if group else None

    async def update_preferences(self, user_id: str, food_preferences: FoodPreferences, play_preferences: PlayPreferences) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "food_preferences": food_preferences.dict(),
                "play_preferences": play_preferences.dict()
            }}
        )
        
        if result.modified_count > 0:
            user = await self.get_user(user_id)
            if user and user.group_ids:
                from app.services.group_service import GroupService
                group_service = GroupService(self.db.client)
                for group_id in user.group_ids:
                    await group_service.calculate_and_update_group_preferences(group_id)

        return result.modified_count > 0
