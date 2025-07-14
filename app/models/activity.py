from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
from bson import ObjectId
from app.core.enums import (
    ActivityType,
    FoodIngredient,
    FoodTaste,
    FoodCookingMethod,
    FoodCuisineType
)

class GeoJson(BaseModel):
    type: str = Field(default="Point")
    coordinates: List[float] = Field(..., description="[경도, 위도] 순서")

class FoodAttributes(BaseModel):
    cuisine_types: List[FoodCuisineType] = Field(default=[], description="요리 종류")
    ingredients: List[FoodIngredient] = Field(default=[], description="주재료")
    tastes: List[FoodTaste] = Field(default=[], description="맛")
    cooking_methods: List[FoodCookingMethod] = Field(default=[], description="조리법")

class PlayAttributes(BaseModel):
    crowd_level: float = Field(default=0.0, ge=-1, le=1)
    activeness_level: float = Field(default=0.0, ge=-1, le=1)
    trend_level: float = Field(default=0.0, ge=-1, le=1)
    planning_level: float = Field(default=0.0, ge=-1, le=1)
    location_preference: float = Field(default=0.0, ge=-1, le=1)
    vibe_level: float = Field(default=0.0, ge=-1, le=1)

class ActivityModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    name: str = Field(..., description="활동의 이름 (예: A1그릴, 히어로보드게임카페)")
    type: ActivityType = Field(..., description="FOOD 또는 ACTIVITY 타입")
    category_id: str = Field(..., description="CategoryModel의 ID")
    location: Optional[GeoJson] = None
    
    # 활동 타입에 따라 둘 중 하나의 속성을 가짐
    food_attributes: Optional[FoodAttributes] = None
    play_attributes: Optional[PlayAttributes] = None
    
    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {"id": str}