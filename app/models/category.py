from pydantic import BaseModel, Field
from typing import Optional


class CategoryModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    name: str = Field(..., description="카테고리 이름 (예: 운동, 식사, 스터디)")
    description: Optional[str] = Field(None, description="카테고리 설명")

    class Config:
        from_attributes = True
        validate_by_name = True
        json_encoders = {"id": str}
