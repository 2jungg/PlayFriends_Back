from enum import Enum

class ActivityType(str, Enum):
    FOOD = "음식"
    ACTIVITY = "놀거리"

class FoodIngredient(str, Enum):
    MEAT = "고기"
    VEGETABLE = "채소"
    FISH = "생선"
    MILK = "우유"
    EGG = "계란"
    FLOUR = "밀가루"

class FoodTaste(str, Enum):
    SPICY = "매운"
    GREASY = "느끼한"
    SWEET = "단"
    SALTY = "짠"
    BITTER = "쓴"
    SOUR = "신"

class FoodCookingMethod(str, Enum):
    SOUP = "국물"
    GRILL = "구이"
    STEAMED = "찜/찌개"
    STIR_FRIED = "볶음"
    FRIED = "튀김"
    LIQUID = "음료"

class FoodCuisineType(str, Enum):
    KOREAN = "한식"
    CHINESE = "중식"
    JAPANESE = "일식"
    WESTERN = "양식"
    SOUTEAST_ASIAN = "동남아식"
