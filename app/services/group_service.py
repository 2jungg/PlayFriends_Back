import datetime
from collections import defaultdict
from typing import List, Optional

import numpy as np
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.group import GroupModel
from app.models.category import CategoryModel
from app.models.activity import ActivityModel
from app.models.schedule import ScheduleModel, ScheduledActivity, ListScheduleModel
from app.schemas.user import FoodPreferences, PlayPreferences
from app.schemas.group import GroupCreate, GroupUpdate
from app.core.config import settings
from app.core.enums import ActivityType
from app.services.user_service import UserService

class GroupService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client[settings.MONGO_DATABASE]
        self.collection = self.db.groups
        self.users_collection = self.db.users
        self.categories_collection = self.db.categories
        self.activities_collection = self.db.activities
        self.schedules_collection = self.db.schedules
        self.user_service = UserService(db_client)

    def _euclidean_distance(self, v1, v2):
        """두 벡터 간의 유클리드 거리를 계산합니다."""
        v1 = np.array(v1)
        v2 = np.array(v2)
        return np.linalg.norm(v1 - v2)

    async def create_group(self, group_data: GroupCreate, owner_id: str) -> GroupModel:
        group_dict = group_data.dict()
        group_dict["owner_id"] = owner_id
        group_dict["member_ids"] = [owner_id]

        # Fetch owner's preferences and set them as the initial group preferences
        owner = await self.user_service.get_user(owner_id)
        if owner:
            group_dict["food_preferences"] = owner.food_preferences.dict()
            group_dict["play_preferences"] = owner.play_preferences.dict()
        
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

        # Recalculate group preferences
        await self.calculate_and_update_group_preferences(group_id)

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

        # Recalculate group preferences
        await self.calculate_and_update_group_preferences(group_id)

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

    async def calculate_and_update_group_preferences(self, group_id: str) -> Optional[GroupModel]:
        group = await self.get_group(group_id)
        if not group or not group.member_ids:
            return None

        num_members = len(group.member_ids)
        
        # Food preferences calculation
        total_food_scores = defaultdict(lambda: defaultdict(float))
        # Play preferences calculation
        total_play_scores = defaultdict(float)

        for member_id in group.member_ids:
            user = await self.user_service.get_user(member_id)
            if user:
                # Accumulate food preferences scores
                for pref_type in ['ingredients', 'tastes', 'cooking_methods', 'cuisine_types']:
                    for preference in getattr(user.food_preferences, pref_type):
                        total_food_scores[pref_type][preference.name.value] += preference.score
                
                # Accumulate play preferences scores
                for attr, value in user.play_preferences.dict().items():
                    total_play_scores[attr] += value

        # Calculate average food preferences
        avg_food_prefs = FoodPreferences()
        for pref_type in ['ingredients', 'tastes', 'cooking_methods', 'cuisine_types']:
            for preference in getattr(avg_food_prefs, pref_type):
                preference.score = total_food_scores[pref_type][preference.name.value] / num_members

        # Calculate average play preferences
        avg_play_prefs = PlayPreferences()
        for attr in avg_play_prefs.dict().keys():
            setattr(avg_play_prefs, attr, total_play_scores[attr] / num_members)

        # Update group with calculated preferences
        updated_group = await self.update_group(group_id, GroupUpdate(
            food_preferences=avg_food_prefs,
            play_preferences=avg_play_prefs
        ))
        
        return updated_group

    async def recommend_categories(self, group_id: str, top_n: int = 5) -> List[CategoryModel]:
        group = await self.get_group(group_id)
        if not group:
            return []

        time_based_recommendations = []
        
        # 시간 기반 카테고리 추천
        if group.starttime:
            # 점심 시간 (11:30 ~ 14:00)
            lunch_start = group.starttime.replace(hour=11, minute=30, second=0, microsecond=0)
            lunch_end = group.starttime.replace(hour=14, minute=0, second=0, microsecond=0)
            
            # 저녁 시간 (17:30 ~ 20:00)
            dinner_start = group.starttime.replace(hour=17, minute=30, second=0, microsecond=0)
            dinner_end = group.starttime.replace(hour=20, minute=0, second=0, microsecond=0)

            group_start_time = group.starttime
            group_end_time = group.endtime if group.endtime else group.starttime

            # 식사시간 겹치는지 확인
            is_lunch_time = max(group_start_time, lunch_start) < min(group_end_time, lunch_end)
            is_dinner_time = max(group_start_time, dinner_start) < min(group_end_time, dinner_end)

            if is_lunch_time or is_dinner_time:
                restaurant_category = await self.categories_collection.find_one({"name": "식당"})
                if restaurant_category:
                    time_based_recommendations.append(CategoryModel(**restaurant_category))

            # 음주시간 (20:00 이후)
            if group_start_time >= dinner_end:
                bar_category = await self.categories_collection.find_one({"name": "주점"})
                if bar_category:
                    time_based_recommendations.append(CategoryModel(**bar_category))
        
        group_prefs = group.play_preferences
        if not group_prefs:
            group_with_prefs = await self.calculate_and_update_group_preferences(group_id)
            if not group_with_prefs:
                return time_based_recommendations
            group_prefs = group_with_prefs.play_preferences

        group_vector = list(group_prefs.dict().values())
        
        preference_based_categories = []
        # parent_category_id가 있는 카테고리만 추천 (하위 카테고리)
        query = {
            "type": ActivityType.ACTIVITY.value, 
            "play_attributes": {"$ne": None},
            "parent_category_id": {"$ne": None}
        }
        cursor = self.categories_collection.find(query)
        async for category_doc in cursor:
            category = CategoryModel(**category_doc)
            if category.play_attributes:
                category_vector = list(category.play_attributes.dict().values())
                distance = self._euclidean_distance(group_vector, category_vector)
                preference_based_categories.append((category, distance))
        
        preference_based_categories.sort(key=lambda x: x[1])
        
        # top_n 만큼 선호도 기반 카테고리 선택
        top_preference_categories = [cat for cat, dist in preference_based_categories[:top_n]]

        # 중복 제거 및 최종 목록 생성
        final_recommendations = time_based_recommendations
        existing_ids = {str(c.id) for c in final_recommendations}

        for category in top_preference_categories:
            if str(category.id) not in existing_ids:
                final_recommendations.append(category)
        
        return final_recommendations

    async def create_schedules(self, group_id: str, category_ids: List[str], top_n: int = 4) -> Optional[ListScheduleModel]:
        pass
        
    async def create_schedule_from_categories(self, group_id: str, category_ids: List[str]) -> Optional[ScheduleModel]:
        group = await self.get_group(group_id)
        if not group or not group.starttime:
            return None
        
        group_prefs = group.play_preferences
        if not group_prefs:
            group_with_prefs = await self.calculate_and_update_group_preferences(group_id)
            if not group_with_prefs:
                return None
            group_prefs = group_with_prefs.play_preferences
        
        group_vector = list(group_prefs.dict().values())
        
        selected_activities = []
        for category_id in category_ids:
            best_activity = None
            min_distance = float('inf')

            cursor = self.activities_collection.find({"category_id": category_id, "play_attributes": {"$ne": None}})
            async for activity_doc in cursor:
                activity = ActivityModel(**activity_doc)
                if activity.play_attributes:
                    activity_vector = list(activity.play_attributes.dict().values())
                    distance = self._euclidean_distance(group_vector, activity_vector)
                    if distance < min_distance:
                        min_distance = distance
                        best_activity = activity
            
            if best_activity:
                selected_activities.append(best_activity)

        if not selected_activities:
            return None

        # Distribute time equally among selected activities
        num_activities = len(selected_activities)
        total_duration = (group.endtime - group.starttime).total_seconds()
        duration_per_activity = total_duration / num_activities
        
        scheduled_activities = []
        current_time = group.starttime
        for activity in selected_activities:
            end_time = current_time + datetime.timedelta(seconds=duration_per_activity)
            scheduled_activities.append(ScheduledActivity(
                activity_id=activity.id,
                start_time=current_time,
                end_time=end_time
            ))
            current_time = end_time

        schedule_data = {
            "group_id": group_id,
            "scheduled_activities": [sa.dict() for sa in scheduled_activities]
        }
        
        result = await self.schedules_collection.insert_one(schedule_data)
        new_schedule = await self.schedules_collection.find_one({"_id": result.inserted_id})
        
        return ScheduleModel(**new_schedule) if new_schedule else None

group_service: "GroupService"
