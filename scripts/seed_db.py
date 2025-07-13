import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Dict, Any
from bson import ObjectId

# 프로젝트 루트 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# .env 파일 로드
load_dotenv()

from app.core.config import settings
from app.core.enums import (
    ActivityType,
    FoodIngredient,
    FoodTaste,
    FoodCookingMethod,
    FoodCuisineType,
)
from app.models.category import CategoryModel
from app.models.activity import ActivityModel, FoodAttributes, PlayAttributes
from scripts.dummydata import get_dummy_activities

def seed_data():
    """
    MongoDB에 초기 카테고리와 활동 데이터를 시딩하는 스크립트.
    """
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DATABASE]

    # 기존 데이터 삭제
    db.categories.delete_many({})
    db.activities.delete_many({})
    print("기존 카테고리 및 활동 데이터 삭제 완료")

    category_ids: Dict[str, Any] = {}

    def add_category(name: str, type: ActivityType, parent_name: str = None, play_attributes: PlayAttributes = None):
        parent_id = category_ids.get(parent_name)
        
        if type == ActivityType.ACTIVITY and play_attributes is None:
            play_attributes = PlayAttributes(
                crowd_level=0.0,
                activeness_level=0.0,
                trend_level=0.0,
                planning_level=0.0,
                location_preference=0.0,
                vibe_level=0.0
            )

        category = CategoryModel(name=name, type=type, parent_category_id=parent_id, play_attributes=play_attributes)
        result = db.categories.insert_one(category.model_dump(by_alias=True, exclude_none=True))
        category_ids[name] = str(result.inserted_id)

    # 놀거리(ACTIVITY) 카테고리
    play_categories = {
        "문화생활": ["영화관", "뮤지컬", "연극", "콘서트", "서점"],
        "스포츠관람": ["경기관람"],
        "테마파크": ["놀이공원", "동물원", "워터파크"],
        "쇼핑": ["백화점", "아울렛", "팝업 스토어"],
        "엔터테인먼트": ["피시방", "노래방", "보드게임카페", "방탈출 카페", "당구장", "볼링장"],
        "야외활동": ["산책", "관광", "등산"],
        "특별한 날": ["파티룸", "이색 데이트", "공방 데이트"],
        "기타": ["미술관, 박물관", "만화방"]
    }
    
    # 음식(FOOD) 카테고리
    food_categories = {''
        "식당": [],
        "카페": [],
    }

    for parent, children in play_categories.items():
        add_category(parent, ActivityType.ACTIVITY)
        for child in children:
            add_category(child, ActivityType.ACTIVITY, parent_name=parent)

    for parent, children in food_categories.items():
        add_category(parent, ActivityType.FOOD)
        for child in children:
            add_category(child, ActivityType.FOOD, parent_name=parent)
    
    print("\n카테고리 데이터 삽입 완료")

    # 활동 데이터 생성 및 삽입
    activities = get_dummy_activities(category_ids)

    if activities:
        db.activities.insert_many([activity.model_dump(by_alias=True, exclude_none=True) for activity in activities])
        print("\n활동 데이터 삽입 완료")

        # 각 카테고리의 play_attributes를 계산하고 업데이트
        pipeline = [
            {
                "$match": {
                    "play_attributes": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$category_id",
                    "avg_crowd_level": {"$avg": "$play_attributes.crowd_level"},
                    "avg_activeness_level": {"$avg": "$play_attributes.activeness_level"},
                    "avg_trend_level": {"$avg": "$play_attributes.trend_level"},
                    "avg_planning_level": {"$avg": "$play_attributes.planning_level"},
                    "avg_location_preference": {"$avg": "$play_attributes.location_preference"},
                    "avg_vibe_level": {"$avg": "$play_attributes.vibe_level"}
                }
            }
        ]
        
        category_attributes = db.activities.aggregate(pipeline)
        
        for cat_attrs in category_attributes:
            category_id_str = cat_attrs["_id"]
            if not category_id_str:
                continue
            
            play_attributes = PlayAttributes(
                crowd_level=cat_attrs.get("avg_crowd_level"),
                activeness_level=cat_attrs.get("avg_activeness_level"),
                trend_level=cat_attrs.get("avg_trend_level"),
                planning_level=cat_attrs.get("avg_planning_level"),
                location_preference=cat_attrs.get("avg_location_preference"),
                vibe_level=cat_attrs.get("avg_vibe_level")
            )
            
            db.categories.update_one(
                {"_id": ObjectId(category_id_str)},
                {"$set": {"play_attributes": play_attributes.model_dump(exclude_none=True)}}
            )
        
        print("\n놀거리 카테고리의 PlayAttributes 업데이트 완료")

    client.close()

if __name__ == "__main__":
    seed_data()
    print("\n데이터 시딩 작업이 성공적으로 완료되었습니다.")
