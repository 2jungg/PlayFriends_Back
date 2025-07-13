from pydantic import BaseModel, Field
from typing import Optional
from app.core.enums import ActivityType

class CategoryModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    name: str = Field(..., description="카테고리 이름 (예: 한식, 보드게임)")
    type: ActivityType = Field(..., description="FOOD 또는 ACTIVITY 타입")
    parent_category_id: Optional[str] = Field(default=None, description="상위 카테고리의 ID (계층 구조용)")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {"id": str}