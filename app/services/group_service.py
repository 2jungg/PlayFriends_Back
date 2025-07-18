import datetime
import random
import numpy as np
from collections import defaultdict
from typing import List, Optional
from itertools import permutations, product
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.group import GroupModel
from app.models.category import CategoryModel
from app.models.activity import ActivityModel, FoodAttributes
from app.models.schedule import ScheduledActivity
from app.schemas.schedule import ScheduleSuggestion, ListScheduleResponse
from app.schemas.user import FoodPreferences, PlayPreferences
from app.schemas.category import CategoryListResponse
from app.schemas.group import GroupCreate, GroupUpdate, GroupDetailResponse, GroupMember
from app.core.config import settings
from app.core.enums import ActivityType
from app.services.user_service import UserService
from app.services.gemini_service import GeminiService

class GroupService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client[settings.MONGO_DATABASE]
        self.collection = self.db.groups
        self.users_collection = self.db.users
        self.categories_collection = self.db.categories
        self.activities_collection = self.db.activities
        self.schedules_collection = self.db.schedules
        self.user_service = UserService(db_client)
        self.gemini_service = GeminiService()

    def _euclidean_distance(self, v1, v2):
        """두 벡터 간의 유클리드 거리를 계산합니다."""
        v1 = np.array(v1)
        v2 = np.array(v2)
        return np.linalg.norm(v1 - v2)

    def _calculate_food_similarity_score(self, prefs: FoodPreferences, attrs: FoodAttributes) -> float:
        """음식 선호도와 속성 간의 유사도 점수를 계산합니다."""
        score = 0
        if not prefs or not attrs:
            return 0
        
        pref_dict = {
            'ingredients': {p.name.value: p.score for p in prefs.ingredients},
            'tastes': {p.name.value: p.score for p in prefs.tastes},
            'cooking_methods': {p.name.value: p.score for p in prefs.cooking_methods},
            'cuisine_types': {p.name.value: p.score for p in prefs.cuisine_types}
        }

        attr_dict = {
            'ingredients': [a.value for a in attrs.ingredients],
            'tastes': [a.value for a in attrs.tastes],
            'cooking_methods': [a.value for a in attrs.cooking_methods],
            'cuisine_types': [a.value for a in attrs.cuisine_types]
        }

        for pref_type, preferences in pref_dict.items():
            for pref_name, pref_score in preferences.items():
                if pref_name in attr_dict[pref_type]:
                    score += pref_score

        return score

    def _calculate_food_attraction_score(self, attr1: FoodAttributes, attr2: FoodAttributes) -> float:
        """두 음식 활동 간의 유사도 점수를 계산합니다."""
        if not attr1 or not attr2:
            return 0
        
        score = 0
        attr1_sets = {
            'ingredients': {a.value for a in attr1.ingredients},
            'tastes': {a.value for a in attr1.tastes},
            'cooking_methods': {a.value for a in attr1.cooking_methods},
            'cuisine_types': {a.value for a in attr1.cuisine_types}
        }
        attr2_sets = {
            'ingredients': {a.value for a in attr2.ingredients},
            'tastes': {a.value for a in attr2.tastes},
            'cooking_methods': {a.value for a in attr2.cooking_methods},
            'cuisine_types': {a.value for a in attr2.cuisine_types}
        }

        for key in attr1_sets:
            score += len(attr1_sets[key].intersection(attr2_sets[key]))
        
        # 유사도가 높을수록 거리는 가까워야 하므로 역수로 변환 (0으로 나누는 것 방지)
        return 1 / (1 + score)

    def _jaccard_dissimilarity(self, schedule1: tuple, schedule2: tuple) -> float:
        """두 스케줄 간의 Jaccard 유사도를 계산합니다."""
        set1 = {str(act.id) for act in schedule1[0]}
        set2 = {str(act.id) for act in schedule2[0]}
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        if union == 0:
            return 0.0
        
        return 1.0 - (intersection / union)

    async def _create_group_detail_response(self, group_doc: dict) -> GroupDetailResponse:
        group_model = GroupModel(**group_doc)
        members = []
        for member_id in group_model.member_ids:
            user = await self.user_service.get_user(member_id)
            if user:
                members.append(GroupMember(id=str(user.id), name=user.username))
        
        group_detail = GroupDetailResponse(**group_model.dict(), members=members)
        return group_detail

    async def create_group(self, group_data: GroupCreate, owner_id: str) -> GroupDetailResponse:
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

        new_group_doc = await self.collection.find_one({"_id": new_group_id})
        return await self._create_group_detail_response(new_group_doc)

    async def get_group(self, group_id: str) -> Optional[GroupDetailResponse]:
        group_doc = await self.collection.find_one({"_id": ObjectId(group_id)})
        if group_doc:
            return await self._create_group_detail_response(group_doc)
        return None

    async def get_all_groups(self) -> List[GroupDetailResponse]:
        groups = []
        cursor = self.collection.find()
        async for group_doc in cursor:
            groups.append(await self._create_group_detail_response(group_doc))
        return groups

    async def update_group(self, group_id: str, group_data: GroupUpdate) -> Optional[GroupDetailResponse]:
        update_data = {k: v for k, v in group_data.dict().items() if v is not None}
        
        if not update_data:
            return await self.get_group(group_id)

        await self.collection.update_one(
            {"_id": ObjectId(group_id)},
            {"$set": update_data}
        )
        return await self.get_group(group_id)

    async def delete_group(self, group_id: str) -> bool:
        group_doc = await self.collection.find_one({"_id": ObjectId(group_id)})
        if not group_doc:
            return False
        group = GroupModel(**group_doc)

        # Remove group_id from all members' group_ids list
        await self.user_service.remove_group_from_all_users(group.member_ids, group_id)

        result = await self.collection.delete_one({"_id": ObjectId(group_id)})
        return result.deleted_count > 0

    async def add_member(self, group_id: str, user_id: str) -> bool:
        group_doc = await self.collection.find_one({"_id": ObjectId(group_id)})
        if not group_doc:
            return False
        group = GroupModel(**group_doc)
        if user_id in group.member_ids:
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
        group_doc = await self.collection.find_one({"_id": ObjectId(group_id)})
        if not group_doc:
            return False
        group = GroupModel(**group_doc)
        # Cannot remove the owner or a user not in the group
        if user_id not in group.member_ids or user_id == group.owner_id:
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

    async def calculate_and_update_group_preferences(self, group_id: str) -> Optional[GroupDetailResponse]:
        group_doc = await self.collection.find_one({"_id": ObjectId(group_id)})
        if not group_doc:
            return None
        group = GroupModel(**group_doc)
        if not group.member_ids:
            return await self._create_group_detail_response(group_doc)

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

    async def recommend_categories(self, group_id: str, top_n: int = 5) -> CategoryListResponse:
        group_doc = await self.collection.find_one({"_id": ObjectId(group_id)})
        if not group_doc:
            return CategoryListResponse(categories=[])
        group = GroupModel(**group_doc)

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
                return CategoryListResponse(categories=[str(c.name) for c in time_based_recommendations])
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
        existing_ids = {str(c.id) for c in time_based_recommendations}
        final_recommendations = [str(c.name) for c in time_based_recommendations]

        for category in top_preference_categories:
            if str(category.id) not in existing_ids:
                final_recommendations.append(str(category.name))
        
        return CategoryListResponse(categories=final_recommendations)

    async def create_schedules(self, group_id: str, category_names: List[str], top_n: int = 4) -> Optional[ListScheduleResponse]:
        # --- Parameters for recommendation diversity ---
        POOL_SIZE = 10  # Number of activities to select for the final pool
        CANDIDATE_POOL_SIZE = 30  # Number of candidates for sampling
        DIVERSITY_WEIGHT = 0.5  # Weight for the diversity score
        HARMONY_WEIGHT = 1.0  # Weight for the harmony score
        NOVELTY_WEIGHT = 0.3 # Weight for novelty between schedules
        # -----------------------------------------

        group_doc = await self.collection.find_one({"_id": ObjectId(group_id)})
        if not group_doc:
            return None
        group = GroupModel(**group_doc)
        if not group.starttime or not group.endtime:
            return None

        category_ids = []
        for cat_name in category_names:
            category = await self.categories_collection.find_one({"name": cat_name})
            if category:
                category_ids.append(str(category["_id"]))

        group_play_prefs = group.play_preferences
        group_food_prefs = group.food_preferences
        if not group_play_prefs or not group_food_prefs:
            group_with_prefs = await self.calculate_and_update_group_preferences(group_id)
            if not group_with_prefs:
                return None
            group_play_prefs = group_with_prefs.play_preferences
            group_food_prefs = group_with_prefs.food_preferences
        
        group_play_vector = list(group_play_prefs.dict().values())

        activity_pools = []
        for category_id in category_ids:
            category = await self.categories_collection.find_one({"_id": ObjectId(category_id)})
            if not category:
                continue
            
            category_model = CategoryModel(**category)
            activities = []
            cursor = self.activities_collection.find({"category_id": category_id})
            async for activity_doc in cursor:
                activities.append(ActivityModel(**activity_doc))

            if not activities:
                continue

            # Sort activities based on similarity to group preferences
            if category_model.type == ActivityType.ACTIVITY:
                activities.sort(
                    key=lambda act: self._euclidean_distance(group_play_vector, list(act.play_attributes.dict().values())) if act.play_attributes else float('inf')
                )
            elif category_model.type == ActivityType.FOOD:
                activities.sort(
                    key=lambda act: self._calculate_food_similarity_score(group_food_prefs, act.food_attributes) if act.food_attributes else 0,
                    reverse=True
                )
            
            # --- 1. Weighted Random Sampling for Activity Pool ---
            candidate_activities = activities[:CANDIDATE_POOL_SIZE]
            if not candidate_activities:
                continue

            weights = []
            if category_model.type == ActivityType.ACTIVITY:
                # Lower distance is better, so we invert it for weights. Add 1 to avoid division by zero.
                distances = [self._euclidean_distance(group_play_vector, list(act.play_attributes.dict().values())) if act.play_attributes else float('inf') for act in candidate_activities]
                max_dist = max(d for d in distances if d != float('inf')) + 1
                weights = [max_dist - d for d in distances]
            elif category_model.type == ActivityType.FOOD:
                weights = [self._calculate_food_similarity_score(group_food_prefs, act.food_attributes) if act.food_attributes else 0 for act in candidate_activities]

            # Normalize weights to be probabilities
            total_weight = sum(weights)
            if total_weight > 0:
                probabilities = [w / total_weight for w in weights]
                # Use np.random.choice for sampling without replacement
                sampled_indices = np.random.choice(len(candidate_activities), size=min(POOL_SIZE, len(candidate_activities)), p=probabilities, replace=False)
                activity_pools.append([candidate_activities[i] for i in sampled_indices])
            else:
                # If all weights are zero, fall back to top N
                activity_pools.append(candidate_activities[:POOL_SIZE])
            # ----------------------------------------------------

        if not activity_pools:
            return None

        all_combinations = list(product(*activity_pools))

        best_schedules = []
        for combo in all_combinations:
            min_final_score = float('inf')
            best_permutation = None
            
            for p in permutations(combo):
                harmony_score = 0
                diversity_score = 0
                
                # --- 2. Calculate Harmony and Diversity Scores ---
                for i in range(len(p) - 1):
                    act1 = p[i]
                    act2 = p[i+1]

                    if act1.type == ActivityType.ACTIVITY and act2.type == ActivityType.ACTIVITY:
                        dist = self._euclidean_distance(list(act1.play_attributes.dict().values()), list(act2.play_attributes.dict().values()))
                    elif act1.type == ActivityType.FOOD and act2.type == ActivityType.FOOD:
                        dist = self._calculate_food_attraction_score(act1.food_attributes, act2.food_attributes)
                    else:
                        dist = 2.0
                    harmony_score += dist
                
                # Calculate diversity score for the permutation
                if len(p) > 1:
                    total_dist = 0
                    pair_count = 0
                    for i in range(len(p)):
                        for j in range(i + 1, len(p)):
                            act1 = p[i]
                            act2 = p[j]
                            if act1.type == ActivityType.ACTIVITY and act2.type == ActivityType.ACTIVITY:
                                total_dist += self._euclidean_distance(list(act1.play_attributes.dict().values()), list(act2.play_attributes.dict().values()))
                            elif act1.type == ActivityType.FOOD and act2.type == ActivityType.FOOD:
                                total_dist += self._calculate_food_attraction_score(act1.food_attributes, act2.food_attributes)
                            else:
                                total_dist += 2.0
                            pair_count += 1
                    diversity_score = total_dist / pair_count if pair_count > 0 else 0

                final_score = (HARMONY_WEIGHT * harmony_score) - (DIVERSITY_WEIGHT * diversity_score)
                # -------------------------------------------------

                if final_score < min_final_score:
                    min_final_score = final_score
                    best_permutation = p
            
            if best_permutation:
                best_schedules.append((best_permutation, min_final_score))

        best_schedules.sort(key=lambda x: x[1])

        # --- 3. Maximal Marginal Relevance (MMR) for Final Selection ---
        if not best_schedules:
            return None

        selected_schedules = []
        candidate_schedules = best_schedules.copy()

        # Select the first schedule (the best one)
        selected_schedules.append(candidate_schedules.pop(0))

        while len(selected_schedules) < top_n and candidate_schedules:
            next_schedule_idx = -1
            max_mmr_score = -float('inf')

            for i, candidate in enumerate(candidate_schedules):
                original_score = candidate[1]
                
                # Calculate novelty against already selected schedules
                novelty_score = sum(self._jaccard_dissimilarity(candidate, selected) for selected in selected_schedules) / len(selected_schedules)
                
                # MMR score: lower original score is better, so we use -original_score
                mmr_score = -original_score + NOVELTY_WEIGHT * novelty_score
                
                if mmr_score > max_mmr_score:
                    max_mmr_score = mmr_score
                    next_schedule_idx = i
            
            if next_schedule_idx != -1:
                selected_schedules.append(candidate_schedules.pop(next_schedule_idx))
        # ----------------------------------------------------------------

        final_schedules = []
        
        for activities, score in selected_schedules:
            if not activities:
                continue

            # Call Gemini API to get a realistic schedule
            gemini_schedule = await self.gemini_service.generate_realistic_schedule(list(activities), group.starttime, group.endtime)
            
            response_activities = []
            
            if gemini_schedule:
                # Use the schedule from Gemini
                activity_map = {str(act.id): act for act in activities}
                for item in gemini_schedule:
                    activity_obj = activity_map.get(item['activity_id'])
                    if activity_obj:
                        _cat = await self.categories_collection.find_one({"_id": ObjectId(activity_obj.category_id)})
                        from app.schemas.schedule import ScheduledActivity as ResponseScheduledActivity
                        response_activities.append(ResponseScheduledActivity(
                            name=activity_obj.name,
                            category=_cat["name"],
                            start_time=item['start_time'],
                            end_time=item['end_time'],
                            location=activity_obj.location
                        ))
            else:
                # Fallback to simple time division if Gemini fails
                total_duration = (group.endtime - group.starttime).total_seconds()
                num_activities = len(activities)
                if num_activities == 0: continue
                duration_per_activity = total_duration / num_activities
                
                current_time = group.starttime
                for activity_obj in activities:
                    end_time = current_time + datetime.timedelta(seconds=duration_per_activity)
                    _cat = await self.categories_collection.find_one({"_id": ObjectId(activity_obj.category_id)})
                    from app.schemas.schedule import ScheduledActivity as ResponseScheduledActivity
                    response_activities.append(ResponseScheduledActivity(
                        name=activity_obj.name,
                        category=_cat["name"],
                        start_time=current_time,
                        end_time=end_time,
                        location=activity_obj.location
                    ))
                    current_time = end_time

            if response_activities:
                schedule_suggestion = ScheduleSuggestion(
                    group_id=group_id,
                    scheduled_activities=response_activities
                )
                final_schedules.append(schedule_suggestion)

        if not final_schedules:
            return None
            
        return ListScheduleResponse(schedules=final_schedules)

group_service: "GroupService"
