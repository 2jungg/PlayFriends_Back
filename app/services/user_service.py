from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.user import UserCreate, FoodPreferences, PlayPreferences
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

    async def get_user_groups(self, user: UserModel) -> List[GroupModel]:
        group_ids_as_obj = [ObjectId(gid) for gid in user.group_ids]
        groups_cursor = self.group_collection.find({"_id": {"$in": group_ids_as_obj}})
        groups = await groups_cursor.to_list(length=None)
        return [GroupModel(**g) for g in groups]

    async def update_preferences(self, user_id: str, food_preferences: FoodPreferences, play_preferences: PlayPreferences) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "food_preferences": food_preferences.dict(),
                "play_preferences": play_preferences.dict()
            }}
        )
        return result.modified_count > 0
