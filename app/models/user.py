from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Any
from bson import ObjectId
from app.schemas.user import FoodPreferences, PlayPreferences

class UserModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    userid: str = Field(..., description="고유한 사용자 ID (Unique Index 필요)")
    username: str = Field(..., description="사용자 이름")
    hashed_password: str
    is_active: bool = Field(True)
    
    food_preferences: FoodPreferences = Field(default_factory=FoodPreferences)
    play_preferences: PlayPreferences = Field(default_factory=PlayPreferences)
    
    group_ids: List[str] = Field(default=[], description="사용자가 속한 Group ID 목록")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        from_attributes = True
        populate_by_name = True
        validate_by_name = True
        json_encoders = {"id": str}
