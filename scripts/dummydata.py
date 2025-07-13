from app.models.activity import ActivityModel, FoodAttributes, PlayAttributes, GeoJson
from app.core.enums import (
    ActivityType,
    FoodIngredient,
    FoodTaste,
    FoodCookingMethod,
    FoodCuisineType,
)

def get_dummy_activities(category_ids):
    """
    대전 지역의 활동 더미 데이터를 반환하는 함수.
    """
    activities = [
        # === 놀거리 (Activity) ===
        # --- 공원 & 자연 ---
        ActivityModel(name="한밭수목원", type=ActivityType.ACTIVITY, category_id=category_ids.get("산책"), location=GeoJson(coordinates=[127.3859, 36.3699]), play_attributes=PlayAttributes(crowd_level=-0.5, activeness_level=-0.7, location_preference=-1.0, vibe_level=-0.8)),
        ActivityModel(name="장태산자연휴양림", type=ActivityType.ACTIVITY, category_id=category_ids.get("야외활동"), location=GeoJson(coordinates=[127.3332, 36.2204]), play_attributes=PlayAttributes(crowd_level=-0.6, activeness_level=0.2, location_preference=-1.0, vibe_level=-0.9)),
        ActivityModel(name="뿌리공원", type=ActivityType.ACTIVITY, category_id=category_ids.get("관광"), location=GeoJson(coordinates=[127.4031, 36.2884]), play_attributes=PlayAttributes(crowd_level=0.1, activeness_level=-0.2, location_preference=-0.8, vibe_level=-0.4)),
        ActivityModel(name="상소동 산림욕장", type=ActivityType.ACTIVITY, category_id=category_ids.get("야외활동"), location=GeoJson(coordinates=[127.4942, 36.2446]), play_attributes=PlayAttributes(crowd_level=-0.7, activeness_level=0.3, location_preference=-1.0, vibe_level=-0.9)),
        ActivityModel(name="대청호 오백리길", type=ActivityType.ACTIVITY, category_id=category_ids.get("산책"), location=GeoJson(coordinates=[127.484, 36.474]), play_attributes=PlayAttributes(crowd_level=-0.8, activeness_level=0.5, location_preference=-1.0, vibe_level=-0.7)),
        ActivityModel(name="계족산 황톳길", type=ActivityType.ACTIVITY, category_id=category_ids.get("등산"), location=GeoJson(coordinates=[127.462, 36.391]), play_attributes=PlayAttributes(crowd_level=-0.4, activeness_level=0.6, location_preference=-1.0, vibe_level=-0.6)),
        ActivityModel(name="유림공원", type=ActivityType.ACTIVITY, category_id=category_ids.get("산책"), location=GeoJson(coordinates=[127.3801, 36.3682]), play_attributes=PlayAttributes(crowd_level=-0.2, activeness_level=-0.6, location_preference=-0.9, vibe_level=-0.5)),
        ActivityModel(name="보문산", type=ActivityType.ACTIVITY, category_id=category_ids.get("등산"), location=GeoJson(coordinates=[127.418, 36.304]), play_attributes=PlayAttributes(crowd_level=-0.3, activeness_level=0.7, location_preference=-1.0, vibe_level=-0.5)),
        ActivityModel(name="우암사적공원", type=ActivityType.ACTIVITY, category_id=category_ids.get("관광"), location=GeoJson(coordinates=[127.447, 36.341]), play_attributes=PlayAttributes(crowd_level=-0.7, activeness_level=-0.8, location_preference=-0.7, vibe_level=-0.9)),
        ActivityModel(name="대동하늘공원", type=ActivityType.ACTIVITY, category_id=category_ids.get("관광"), location=GeoJson(coordinates=[127.442, 36.336]), play_attributes=PlayAttributes(crowd_level=0.2, activeness_level=-0.5, trend_level=0.4, location_preference=-0.8, vibe_level=0.3)),

        # --- 박물관 & 미술관 ---
        ActivityModel(name="국립중앙과학관", type=ActivityType.ACTIVITY, category_id=category_ids.get("미술관, 박물관"), location=GeoJson(coordinates=[127.385, 36.377]), play_attributes=PlayAttributes(crowd_level=0.3, activeness_level=-0.3, location_preference=1.0, vibe_level=-0.2)),
        ActivityModel(name="대전시립미술관", type=ActivityType.ACTIVITY, category_id=category_ids.get("미술관, 박물관"), location=GeoJson(coordinates=[127.386, 36.372]), play_attributes=PlayAttributes(crowd_level=0.1, activeness_level=-0.9, trend_level=0.2, location_preference=1.0, vibe_level=-0.7)),
        ActivityModel(name="이응노미술관", type=ActivityType.ACTIVITY, category_id=category_ids.get("미술관, 박물관"), location=GeoJson(coordinates=[127.384, 36.372]), play_attributes=PlayAttributes(crowd_level=0.0, activeness_level=-0.9, trend_level=0.5, location_preference=1.0, vibe_level=-0.6)),
        ActivityModel(name="화폐박물관", type=ActivityType.ACTIVITY, category_id=category_ids.get("미술관, 박물관"), location=GeoJson(coordinates=[127.383, 36.381]), play_attributes=PlayAttributes(crowd_level=-0.2, activeness_level=-0.8, location_preference=1.0, vibe_level=-0.5)),
        ActivityModel(name="지질박물관", type=ActivityType.ACTIVITY, category_id=category_ids.get("미술관, 박물관"), location=GeoJson(coordinates=[127.380, 36.388]), play_attributes=PlayAttributes(crowd_level=-0.1, activeness_level=-0.7, location_preference=1.0, vibe_level=-0.4)),
        ActivityModel(name="대전근현대사전시관", type=ActivityType.ACTIVITY, category_id=category_ids.get("미술관, 박물관"), location=GeoJson(coordinates=[127.425, 36.328]), play_attributes=PlayAttributes(crowd_level=-0.3, activeness_level=-0.8, location_preference=1.0, vibe_level=-0.6)),

        # --- 테마파크 & 엔터테인먼트 ---
        ActivityModel(name="대전 오월드", type=ActivityType.ACTIVITY, category_id=category_ids.get("테마파크"), location=GeoJson(coordinates=[127.3969, 36.2924]), play_attributes=PlayAttributes(crowd_level=0.7, activeness_level=0.8, trend_level=0.5, vibe_level=0.9)),
        ActivityModel(name="대전 아쿠아리움", type=ActivityType.ACTIVITY, category_id=category_ids.get("동물원"), location=GeoJson(coordinates=[127.418, 36.308]), play_attributes=PlayAttributes(crowd_level=0.6, activeness_level=-0.1, location_preference=1.0, vibe_level=0.5)),
        ActivityModel(name="엑스포 과학공원 한빛탑", type=ActivityType.ACTIVITY, category_id=category_ids.get("관광"), location=GeoJson(coordinates=[127.3863, 36.3763]), play_attributes=PlayAttributes(crowd_level=0.1, activeness_level=-0.4, trend_level=-0.2, location_preference=-0.5)),
        ActivityModel(name="CGV 대전터미널", type=ActivityType.ACTIVITY, category_id=category_ids.get("영화관"), location=GeoJson(coordinates=[127.4323, 36.3523]), play_attributes=PlayAttributes(crowd_level=0.4, activeness_level=-0.9, location_preference=1.0, vibe_level=-0.5)),
        ActivityModel(name="메가박스 대전신세계", type=ActivityType.ACTIVITY, category_id=category_ids.get("영화관"), location=GeoJson(coordinates=[127.385, 36.375]), play_attributes=PlayAttributes(crowd_level=0.6, activeness_level=-0.9, trend_level=0.7, location_preference=1.0, vibe_level=-0.4)),
        ActivityModel(name="타임월드 보드게임카페", type=ActivityType.ACTIVITY, category_id=category_ids.get("보드게임카페"), location=GeoJson(coordinates=[127.3828, 36.3522]), play_attributes=PlayAttributes(crowd_level=0.2, activeness_level=0.1, planning_level=-0.5, location_preference=1.0, vibe_level=0.4)),
        ActivityModel(name="궁동 로데오거리", type=ActivityType.ACTIVITY, category_id=category_ids.get("쇼핑"), location=GeoJson(coordinates=[127.346, 36.362]), play_attributes=PlayAttributes(crowd_level=0.8, activeness_level=0.3, trend_level=0.8, location_preference=-0.2, vibe_level=0.7)),
        ActivityModel(name="으능정이 문화의 거리", type=ActivityType.ACTIVITY, category_id=category_ids.get("쇼핑"), location=GeoJson(coordinates=[127.428, 36.329]), play_attributes=PlayAttributes(crowd_level=0.9, activeness_level=0.2, trend_level=0.6, location_preference=-0.4, vibe_level=0.8)),
        ActivityModel(name="대전 스카이로드", type=ActivityType.ACTIVITY, category_id=category_ids.get("관광"), location=GeoJson(coordinates=[127.428, 36.328]), play_attributes=PlayAttributes(crowd_level=0.7, activeness_level=-0.6, trend_level=0.5, location_preference=-0.5, vibe_level=0.6)),
        ActivityModel(name="소제동 카페거리", type=ActivityType.ACTIVITY, category_id=category_ids.get("이색 데이트"), location=GeoJson(coordinates=[127.433, 36.333]), play_attributes=PlayAttributes(crowd_level=0.5, activeness_level=-0.5, trend_level=0.9, location_preference=-0.3, vibe_level=0.5)),
        ActivityModel(name="대흥동 문화예술의 거리", type=ActivityType.ACTIVITY, category_id=category_ids.get("이색 데이트"), location=GeoJson(coordinates=[127.426, 36.325]), play_attributes=PlayAttributes(crowd_level=0.3, activeness_level=-0.6, trend_level=0.4, location_preference=-0.4, vibe_level=0.2)),
        ActivityModel(name="유성온천 족욕체험장", type=ActivityType.ACTIVITY, category_id=category_ids.get("이색 데이트"), location=GeoJson(coordinates=[127.352, 36.354]), play_attributes=PlayAttributes(crowd_level=-0.1, activeness_level=-0.8, location_preference=-0.7, vibe_level=-0.9)),
        ActivityModel(name="대전시민천문대", type=ActivityType.ACTIVITY, category_id=category_ids.get("문화생활"), location=GeoJson(coordinates=[127.380, 36.391]), play_attributes=PlayAttributes(crowd_level=-0.4, activeness_level=-0.9, location_preference=1.0, vibe_level=-0.7)),
        ActivityModel(name="대전월드컵경기장", type=ActivityType.ACTIVITY, category_id=category_ids.get("경기관람"), location=GeoJson(coordinates=[127.341, 36.369]), play_attributes=PlayAttributes(crowd_level=0.8, activeness_level=-0.2, vibe_level=0.9)),
        ActivityModel(name="한화생명이글스파크", type=ActivityType.ACTIVITY, category_id=category_ids.get("경기관람"), location=GeoJson(coordinates=[127.419, 36.318]), play_attributes=PlayAttributes(crowd_level=0.8, activeness_level=-0.2, vibe_level=0.9)),
    ]
    activities.extend([
        # === 음식 (Food) ===
        # --- 한식 ---
        ActivityModel(name="성심당 본점", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.4288, 36.3279]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.GRAIN], tastes=[FoodTaste.SWEET], cooking_methods=[FoodCookingMethod.ROASTED])),
        ActivityModel(name="오씨칼국수", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.4196, 36.3345]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.SEAFOOD, FoodIngredient.NOODLE], tastes=[FoodTaste.SPICY, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="태평소국밥", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.3957, 36.3365]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.MEAT, FoodIngredient.RICE], tastes=[FoodTaste.SAVORY, FoodTaste.CLEAN], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="광천식당", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.4291, 36.3268]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.SEAFOOD], tastes=[FoodTaste.SPICY], cooking_methods=[FoodCookingMethod.ROASTED])),
        ActivityModel(name="진로집", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.428, 36.325]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.VEGETABLE], tastes=[FoodTaste.SPICY, FoodTaste.SWEET], cooking_methods=[FoodCookingMethod.ROASTED])),
        ActivityModel(name="대선칼국수", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.383, 36.352]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.NOODLE], tastes=[FoodTaste.CLEAN, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="한영식당", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.412, 36.312]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.MEAT], tastes=[FoodTaste.SPICY, FoodTaste.SWEET], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="사리원면옥", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.425, 36.329]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.MEAT, FoodIngredient.NOODLE], tastes=[FoodTaste.CLEAN], cooking_methods=[FoodCookingMethod.RAW])),
        ActivityModel(name="전미원", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.340, 36.318]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.MEAT], tastes=[FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.GRILLED])),

        # --- 양식, 중식, 일식, 기타 ---
        ActivityModel(name="컬리나리아", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.350, 36.360]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.NOODLE, FoodIngredient.SEAFOOD], tastes=[FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.ROASTED])),
        ActivityModel(name="동북아", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.434, 36.332]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.CHINESE], ingredients=[FoodIngredient.MEAT, FoodIngredient.NOODLE], tastes=[FoodTaste.SPICY, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="치앙마이방콕", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.433, 36.331]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ASIAN], ingredients=[FoodIngredient.NOODLE, FoodIngredient.SEAFOOD], tastes=[FoodTaste.SOUR, FoodTaste.SWEET], cooking_methods=[FoodCookingMethod.ROASTED])),
        ActivityModel(name="룸비니", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.345, 36.363]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ASIAN], ingredients=[FoodIngredient.MEAT, FoodIngredient.VEGETABLE], tastes=[FoodTaste.SPICY, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.STEAMED])),
        ActivityModel(name="타코앤칩스", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.381, 36.353]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.MEXICAN], ingredients=[FoodIngredient.MEAT, FoodIngredient.VEGETABLE], tastes=[FoodTaste.SALTY, FoodTaste.SOUR], cooking_methods=[FoodCookingMethod.RAW])),
        ActivityModel(name="라쿠시나에비노", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.378, 36.355]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.DAIRY, FoodIngredient.NOODLE], tastes=[FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.ROASTED])),

        # --- 카페 & 디저트 ---
        ActivityModel(name="풍류소제", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.432, 36.332]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.BITTER])),
        ActivityModel(name="두두당", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.435, 36.331]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.CLEAN])),
        ActivityModel(name="공간태리", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.341, 36.316]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.BITTER, FoodTaste.SOUR])),
        ActivityModel(name="서로히", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.383, 36.351]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.DAIRY])),
        ActivityModel(name="알로하녹", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.362, 36.358]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.CLEAN])),
        ActivityModel(name="롤라", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.490, 36.470]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.BITTER])),
        ActivityModel(name="점선면", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.430, 36.326]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.GRAIN], tastes=[FoodTaste.SWEET, FoodTaste.SALTY])),
        ActivityModel(name="프랭크커핀바", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.375, 36.354]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.BITTER, FoodTaste.SWEET])),
    ])
    activities.extend([
        # === 추가 놀거리 (Activity) ===
        # --- 쇼핑 ---
        ActivityModel(name="갤러리아타임월드", type=ActivityType.ACTIVITY, category_id=category_ids.get("쇼핑"), location=GeoJson(coordinates=[127.382, 36.352]), play_attributes=PlayAttributes(crowd_level=0.7, trend_level=0.8, location_preference=1.0)),
        ActivityModel(name="대전신세계 Art & Science", type=ActivityType.ACTIVITY, category_id=category_ids.get("쇼핑"), location=GeoJson(coordinates=[127.385, 36.375]), play_attributes=PlayAttributes(crowd_level=0.8, trend_level=0.9, location_preference=1.0)),
        ActivityModel(name="현대프리미엄아울렛 대전점", type=ActivityType.ACTIVITY, category_id=category_ids.get("쇼핑"), location=GeoJson(coordinates=[127.398, 36.408]), play_attributes=PlayAttributes(crowd_level=0.6, trend_level=0.5, location_preference=-0.5)),
        ActivityModel(name="은행동 지하상가", type=ActivityType.ACTIVITY, category_id=category_ids.get("쇼핑"), location=GeoJson(coordinates=[127.428, 36.329]), play_attributes=PlayAttributes(crowd_level=0.9, trend_level=0.2, location_preference=1.0)),
        ActivityModel(name="대전 중앙시장", type=ActivityType.ACTIVITY, category_id=category_ids.get("쇼핑"), location=GeoJson(coordinates=[127.432, 36.331]), play_attributes=PlayAttributes(crowd_level=0.9, trend_level=-0.5, location_preference=-0.7)),

        # --- 엔터테인먼트 ---
        ActivityModel(name="락휴 코인노래연습장 둔산점", type=ActivityType.ACTIVITY, category_id=category_ids.get("노래방"), location=GeoJson(coordinates=[127.380, 36.353]), play_attributes=PlayAttributes(crowd_level=0.5, activeness_level=0.7, vibe_level=0.8)),
        ActivityModel(name="레드버튼 보드게임카페 둔산점", type=ActivityType.ACTIVITY, category_id=category_ids.get("보드게임카페"), location=GeoJson(coordinates=[127.381, 36.354]), play_attributes=PlayAttributes(crowd_level=0.4, activeness_level=0.1, planning_level=-0.4, vibe_level=0.5)),
        ActivityModel(name="이스케이프탑 대전점 (방탈출)", type=ActivityType.ACTIVITY, category_id=category_ids.get("방탈출 카페"), location=GeoJson(coordinates=[127.383, 36.355]), play_attributes=PlayAttributes(crowd_level=0.2, activeness_level=0.5, planning_level=0.8, vibe_level=0.7)),
        ActivityModel(name="둔산그랜드볼링센터", type=ActivityType.ACTIVITY, category_id=category_ids.get("볼링장"), location=GeoJson(coordinates=[127.375, 36.351]), play_attributes=PlayAttributes(crowd_level=0.3, activeness_level=0.8, vibe_level=0.6)),
        ActivityModel(name="벌툰 만화카페 은행점", type=ActivityType.ACTIVITY, category_id=category_ids.get("만화방"), location=GeoJson(coordinates=[127.427, 36.328]), play_attributes=PlayAttributes(crowd_level=-0.2, activeness_level=-0.8, location_preference=1.0, vibe_level=-0.7)),

        # === 추가 음식 (Food) ===
        # --- 한식 ---
        ActivityModel(name="오문창순대국밥", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.415, 36.345]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.MEAT], tastes=[FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="소나무집", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.443, 36.361]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.NOODLE], tastes=[FoodTaste.SPICY, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="개천식당", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.430, 36.330]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.MEAT], tastes=[FoodTaste.SWEET, FoodTaste.SALTY], cooking_methods=[FoodCookingMethod.STEAMED])),
        ActivityModel(name="바다황제", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.375, 36.358]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.SEAFOOD], tastes=[FoodTaste.SPICY, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),

        # --- 양식, 중식, 일식, 기타 ---
        ActivityModel(name="맨오브워", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.359, 36.362]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.MEAT], tastes=[FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.GRILLED])),
        ActivityModel(name="잇마이타이", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.348, 36.363]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ASIAN], ingredients=[FoodIngredient.SEAFOOD, FoodIngredient.NOODLE], tastes=[FoodTaste.SPICY, FoodTaste.SOUR], cooking_methods=[FoodCookingMethod.ROASTED])),
        ActivityModel(name="스바라시라멘", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.345, 36.361]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.JAPANESE], ingredients=[FoodIngredient.MEAT, FoodIngredient.NOODLE], tastes=[FoodTaste.SALTY, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="부연부", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.426, 36.327]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.CHINESE], ingredients=[FoodIngredient.MEAT, FoodIngredient.VEGETABLE], tastes=[FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.FRIED])),

        # --- 추가 카페 & 디저트 ---
        ActivityModel(name="카페그레이", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.380, 36.350]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.BITTER])),
        ActivityModel(name="커피인터뷰", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.344, 36.365]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.BITTER, FoodTaste.SOUR])),
        ActivityModel(name="관저당", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.335, 36.305]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.CLEAN])),
        ActivityModel(name="하치카페", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.420, 36.320]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.DAIRY])),
        ActivityModel(name="모루", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.388, 36.351]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.CLEAN]))
    ])
    activities.extend([
        # === 마지막 추가 데이터 ===
        # --- 놀거리 ---
        ActivityModel(name="대전예술의전당", type=ActivityType.ACTIVITY, category_id=category_ids.get("문화생활"), location=GeoJson(coordinates=[127.387, 36.370]), play_attributes=PlayAttributes(crowd_level=0.1, activeness_level=-0.9, trend_level=0.3, vibe_level=-0.7)),
        ActivityModel(name="대전 챔피언 1250", type=ActivityType.ACTIVITY, category_id=category_ids.get("테마파크"), location=GeoJson(coordinates=[127.399, 36.409]), play_attributes=PlayAttributes(crowd_level=0.8, activeness_level=0.9, vibe_level=0.9)),
        ActivityModel(name="클라이밍짐 리드", type=ActivityType.ACTIVITY, category_id=category_ids.get("엔터테인먼트"), location=GeoJson(coordinates=[127.378, 36.358]), play_attributes=PlayAttributes(activeness_level=0.9, planning_level=0.2, vibe_level=0.7)),
        ActivityModel(name="향수공방 프루스트", type=ActivityType.ACTIVITY, category_id=category_ids.get("공방 데이트"), location=GeoJson(coordinates=[127.382, 36.353]), play_attributes=PlayAttributes(activeness_level=-0.3, planning_level=0.5, trend_level=0.6, vibe_level=-0.2)),
        ActivityModel(name="대전시립박물관", type=ActivityType.ACTIVITY, category_id=category_ids.get("미술관, 박물관"), location=GeoJson(coordinates=[127.332, 36.369]), play_attributes=PlayAttributes(crowd_level=-0.4, activeness_level=-0.8, vibe_level=-0.8)),

        # --- 음식 ---
        ActivityModel(name="비래키키", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.470, 36.375]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET])),
        ActivityModel(name="인터뷰맨션", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.345, 36.366]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.MEAT, FoodIngredient.DAIRY], tastes=[FoodTaste.SAVORY])),
        ActivityModel(name="우디룸", type=ActivityType.FOOD, category_id=category_ids.get("카페"), location=GeoJson(coordinates=[127.360, 36.357]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.ETC], tastes=[FoodTaste.SWEET, FoodTaste.CLEAN])),
        ActivityModel(name="홀리데이", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.384, 36.351]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.NOODLE], tastes=[FoodTaste.SAVORY, FoodTaste.SOUR])),
        ActivityModel(name="피제리아616", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.349, 36.360]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.WESTERN], ingredients=[FoodIngredient.DAIRY, FoodIngredient.GRAIN], tastes=[FoodTaste.SALTY, FoodTaste.SAVORY])),
        ActivityModel(name="월산본가", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.342, 36.319]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.MEAT], tastes=[FoodTaste.SWEET, FoodTaste.SALTY], cooking_methods=[FoodCookingMethod.GRILLED])),
        ActivityModel(name="카라마데", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.377, 36.356]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.JAPANESE], ingredients=[FoodIngredient.SEAFOOD], tastes=[FoodTaste.CLEAN, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.RAW])),
        ActivityModel(name="아오리라멘 대전점", type=ActivityType.FOOD, category_id=category_ids.get("식당"), location=GeoJson(coordinates=[127.383, 36.354]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.JAPANESE], ingredients=[FoodIngredient.MEAT, FoodIngredient.NOODLE], tastes=[FoodTaste.SALTY, FoodTaste.SAVORY], cooking_methods=[FoodCookingMethod.SOUP])),
        ActivityModel(name="반갱", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.385, 36.351]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.KOREAN], ingredients=[FoodIngredient.VEGETABLE, FoodIngredient.RICE], tastes=[FoodTaste.CLEAN, FoodTaste.SAVORY])),
        ActivityModel(name="토미야", type=ActivityType.FOOD, category_id=category_ids.get("맛집"), location=GeoJson(coordinates=[127.381, 36.350]), food_attributes=FoodAttributes(cuisine_types=[FoodCuisineType.JAPANESE], ingredients=[FoodIngredient.NOODLE, FoodIngredient.FRIED], tastes=[FoodTaste.SAVORY, FoodTaste.CLEAN], cooking_methods=[FoodCookingMethod.FRIED])),
    ])
    return activities