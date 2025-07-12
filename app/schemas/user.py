from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from app.core.enums import (
    FoodIngredient,
    FoodTaste,
    FoodCookingMethod,
    FoodCuisineType,
)

# 각 취향 항목에 맞는 모델 정의
class IngredientPreference(BaseModel):
    name: FoodIngredient
    score: float = Field(default=0.5, ge=0, le=1)

class TastePreference(BaseModel):
    name: FoodTaste
    score: float = Field(default=0.5, ge=0, le=1)

class CookingMethodPreference(BaseModel):
    name: FoodCookingMethod
    score: float = Field(default=0.5, ge=0, le=1)

class CuisineTypePreference(BaseModel):
    name: FoodCuisineType
    score: float = Field(default=0.5, ge=0, le=1)

# 음식 취향 전체를 담는 모델
class FoodPreferences(BaseModel):
    ingredients: List[IngredientPreference] = Field(default_factory=list)
    tastes: List[TastePreference] = Field(default_factory=list)
    cooking_methods: List[CookingMethodPreference] = Field(default_factory=list)
    cuisine_types: List[CuisineTypePreference] = Field(default_factory=list)

# 놀이 취향 전체를 담는 모델
class ActivityPreferences(BaseModel):
    crowd_level: float = Field(default=0.0, ge=-1, le=1, description="붐비는 정도 (-1: 조용, 1: 붐빔)")
    activeness_level: float = Field(default=0.0, ge=-1, le=1, description="활동성 (-1: 관람형, 1: 체험형)")
    trend_level: float = Field(default=0.0, ge=-1, le=1, description="유행 민감도 (-1: 비유행, 1: 유행)")
    planning_level: float = Field(default=0.0, ge=-1, le=1, description="계획성 (-1: 즉흥, 1: 계획)")
    location_preference: float = Field(default=0.0, ge=-1, le=1, description="장소 (-1: 실외, 1: 실내)")
    vibe_level: float = Field(default=0.0, ge=-1, le=1, description="분위기 (-1: 안정, 1: 도파민 추구)")

# 기본 사용자 정보
class UserBase(BaseModel):
    userid: str = Field(..., description="고유한 사용자 ID")
    username: str = Field(..., description="사용자 이름")
    is_active: bool = True

# 사용자 생성 시 받을 데이터
class UserCreate(UserBase):
    password: str

# 사용자 정보 업데이트 시 받을 데이터
class UserUpdate(BaseModel):
    username: str = Field(..., description="사용자 이름")
    food_preferences: Optional[FoodPreferences] = None
    activity_preferences: Optional[ActivityPreferences] = None

# API 응답으로 보낼 사용자 정보
class User(UserBase):
    id: str = Field(alias="_id")
    food_preferences: FoodPreferences = Field(default_factory=FoodPreferences)
    activity_preferences: ActivityPreferences = Field(default_factory=ActivityPreferences)
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {"id": str}
