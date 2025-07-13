from pydantic import BaseModel, Field
from typing import List
from app.models.category import CategoryModel

class CategoryResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
