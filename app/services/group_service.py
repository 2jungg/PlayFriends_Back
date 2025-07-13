from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
import datetime

from app.models.group import GroupModel
from app.schemas.group import GroupCreate, GroupUpdate
from app.core.config import settings
from app.services.user_service import UserService

class GroupService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client[settings.MONGO_DATABASE]
        self.collection = self.db.groups
        self.user_service = UserService(db_client)

    async def create_group(self, group_data: GroupCreate, owner_id: str) -> GroupModel:
        group_dict = group_data.dict()
        group_dict["owner_id"] = owner_id
        group_dict["member_ids"] = [owner_id]
        
        result = await self.collection.insert_one(group_dict)
        new_group_id = result.inserted_id

        await self.user_service.add_group_to_user(owner_id, str(new_group_id))

        new_group = await self.collection.find_one({"_id": new_group_id})
        return GroupModel(**new_group)

    async def get_group(self, group_id: str) -> Optional[GroupModel]:
        group = await self.collection.find_one({"_id": ObjectId(group_id)})
        if group:
            return GroupModel(**group)
        return None

    async def get_all_groups(self) -> List[GroupModel]:
        groups = []
        cursor = self.collection.find()
        async for group in cursor:
            groups.append(GroupModel(**group))
        return groups

    async def update_group(self, group_id: str, group_data: GroupUpdate) -> Optional[GroupModel]:
        update_data = {k: v for k, v in group_data.dict().items() if v is not None}
        
        if not update_data:
            return await self.get_group(group_id)

        await self.collection.update_one(
            {"_id": ObjectId(group_id)},
            {"$set": update_data}
        )
        updated_group = await self.get_group(group_id)
        return updated_group

    async def delete_group(self, group_id: str) -> bool:
        group = await self.get_group(group_id)
        if not group:
            return False

        # Remove group_id from all members' group_ids list
        await self.user_service.remove_group_from_all_users(group.member_ids, group_id)

        result = await self.collection.delete_one({"_id": ObjectId(group_id)})
        return result.deleted_count > 0

    async def add_member(self, group_id: str, user_id: str) -> bool:
        group = await self.get_group(group_id)
        if not group or user_id in group.member_ids:
            return False

        user = await self.user_service.get_user(user_id)
        if not user:
            print(user_id)
            return False

        # Add user to group's member_ids
        group_update_result = await self.collection.update_one(
            {"_id": ObjectId(group_id)},
            {"$addToSet": {"member_ids": user_id}}
        )

        # Add group to user's group_ids
        await self.user_service.add_group_to_user(user_id, group_id)

        return group_update_result.modified_count > 0

    async def remove_member(self, group_id: str, user_id: str) -> bool:
        group = await self.get_group(group_id)
        # Cannot remove the owner or a user not in the group
        if not group or user_id not in group.member_ids or user_id == group.owner_id:
            return False

        # Remove user from group's member_ids
        group_update_result = await self.collection.update_one(
            {"_id": ObjectId(group_id)},
            {"$pull": {"member_ids": user_id}}
        )

        # Remove group from user's group_ids
        await self.user_service.remove_group_from_user(user_id, group_id)

        return group_update_result.modified_count > 0

    async def deactivate_expired_groups(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        query = {
            "is_active": True,
            "$or": [
                {"endtime": {"$ne": None, "$lt": now}},
                {"endtime": None, "starttime": {"$lt": now}}
            ]
        }
        result = await self.collection.update_many(
            query,
            {"$set": {"is_active": False}}
        )
        print(f"Deactivated {result.modified_count} expired groups.")

group_service: "GroupService"
