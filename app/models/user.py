from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from app.schemas.user import FoodPreferences, ActivityPreferences

class UserModel(BaseModel):
    id: str = Field(alias="_id")
    userid: str = Field(..., description="고유한 사용자 ID (Unique Index 필요)")
    username: str = Field(..., description="사용자 이름")
    hashed_password: str
    is_active: bool = True
    food_preferences: FoodPreferences = Field(default_factory=FoodPreferences)
    activity_preferences: ActivityPreferences = Field(default_factory=ActivityPreferences)
    activity_log: List[str] = Field(default=[], description="참여한 활동 ID 목록")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {"id": str}
