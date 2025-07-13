from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from bson import ObjectId
from app.core.enums import ActivityType
from app.models.activity import PlayAttributes

class CategoryModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    name: str = Field(..., description="카테고리 이름 (예: 한식, 보드게임)")
    type: ActivityType = Field(..., description="FOOD 또는 ACTIVITY 타입")
    parent_category_id: Optional[str] = Field(default=None, description="상위 카테고리의 ID (계층 구조용)")
    play_attributes: Optional[PlayAttributes] = Field(default=None, description="놀이 특성")

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
