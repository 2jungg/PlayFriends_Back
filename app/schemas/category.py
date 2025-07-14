from pydantic import BaseModel, Field
from typing import List
from app.models.category import CategoryModel

class CategoryListResponse(BaseModel):
    categories: List[str]
