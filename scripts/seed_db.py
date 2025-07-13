#!/usr/bin/env python
import pymongo
from bson import ObjectId
from app.core.config import Settings

# --- 1. DB 연결 설정 ---
# 실제 환경에서는 환경 변수 등을 사용하는 것이 좋습니다.
MONGO_URI = Settings.MONGO_URI
DB_NAME = Settings.MONGO_DATABASE

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# --- 2. 초기 데이터 정의 ---

# 카테고리 데이터
# parent_category_name 필드는 스크립트 내에서 ID를 찾기 위한 임시 필드입니다.
CATEGORIES = [
    {"name": "한식", "type": "FOOD", "parent_category_name": None},
    {"name": "일식", "type": "FOOD", "parent_category_name": None},
    {"name": "실내활동", "type": "ACTIVITY", "parent_category_name": None},
    {"name": "야외활동", "type": "ACTIVITY", "parent_category_name": None},
    
    {"name": "삼겹살", "type": "FOOD", "parent_category_name": "한식"},
    {"name": "초밥", "type": "FOOD", "parent_category_name": "일식"},
    {"name": "보드게임", "type": "ACTIVITY", "parent_category_name": "실내활동"},
]

# 활동(가게) 데이터
# category_name 필드는 스크립트 내에서 ID를 찾기 위한 임시 필드입니다.
ACTIVITIES = [
    {
        "name": "A1 삼겹살 강남점",
        "type": "FOOD",
        "category_name": "삼겹살",
        "location": {"type": "Point", "coordinates": [127.027, 37.497]},
        "food_attributes": {
            "cuisine_types": ["KOREAN"],
            "ingredients": ["MEAT"],
            "tastes": ["SAVORY", "SALTY"],
            "cooking_methods": ["GRILLED"]
        },
        "play_attributes": {
            "crowd_level": 0.7, "activeness_level": 0.3, "trend_level": -0.2,
            "planning_level": -0.5, "location_preference": 1.0, "vibe_level": 0.6
        }
    },
    {
        "name": "히어로 보드게임카페",
        "type": "ACTIVITY",
        "category_name": "보드게임",
        "location": {"type": "Point", "coordinates": [127.025, 37.499]},
        "food_attributes": None,
        "play_attributes": {
            "crowd_level": 0.2, "activeness_level": -0.3, "trend_level": 0.1,
            "planning_level": 0.4, "location_preference": 1.0, "vibe_level": -0.4
        }
    }
]


def seed_database():
    print("데이터베이스 시딩을 시작합니다...")

    # --- 3. 데이터가 이미 있는지 확인 (멱등성 보장) ---
    # 스크립트를 여러 번 실행해도 데이터가 중복 생성되지 않도록 합니다.
    if db.categories.count_documents({}) > 0:
        print("이미 카테고리 데이터가 존재합니다. 시딩을 건너뜁니다.")
        return

    # --- 4. 카테고리 생성 및 ID 저장 ---
    print("카테고리 생성 중...")
    # parent_category_id를 채우기 위해 먼저 부모 카테고리부터 생성
    parent_categories = [c for c in CATEGORIES if c["parent_category_name"] is None]
    for category_data in parent_categories:
        category_data.pop("parent_category_name", None) # 임시 필드 제거
        db.categories.insert_one(category_data)
    
    # 생성된 부모 카테고리들의 이름과 ID를 매핑
    category_id_map = {doc['name']: doc['_id'] for doc in db.categories.find()}

    # 자식 카테고리 생성
    child_categories = [c for c in CATEGORIES if c["parent_category_name"] is not None]
    for category_data in child_categories:
        parent_name = category_data.pop("parent_category_name")
        parent_id = category_id_map.get(parent_name)
        if parent_id:
            category_data["parent_category_id"] = str(parent_id)
        db.categories.insert_one(category_data)

    print(f"{db.categories.count_documents({})}개의 카테고리가 생성되었습니다.")
    
    # 최종 카테고리 맵 다시 생성
    category_id_map = {doc['name']: str(doc['_id']) for doc in db.categories.find()}

    # --- 5. 활동(Activity) 생성 ---
    print("활동 데이터 생성 중...")
    for activity_data in ACTIVITIES:
        category_name = activity_data.pop("category_name")
        category_id = category_id_map.get(category_name)
        if category_id:
            activity_data["category_id"] = category_id
            db.activities.insert_one(activity_data)
        else:
            print(f"경고: '{category_name}'에 해당하는 카테고리를 찾을 수 없어 '{activity_data['name']}' 활동을 생성하지 못했습니다.")

    print(f"{db.activities.count_documents({})}개의 활동이 생성되었습니다.")
    print("데이터베이스 시딩 완료!")

if __name__ == "__main__":
    seed_database()
