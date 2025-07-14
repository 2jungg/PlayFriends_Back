from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.group import GroupModel
import datetime
from .user import FoodPreferences, PlayPreferences

class GroupCreate(BaseModel):
    groupname: str
    starttime: datetime.datetime
    endtime: Optional[datetime.datetime]

class GroupUpdate(BaseModel):
    groupname: Optional[str] = None
    starttime: Optional[datetime.datetime] = None
    endtime: Optional[datetime.datetime] = None
    is_active: Optional[bool] = None
    member_ids: Optional[List[str]] = None

class GroupResponse(GroupModel):
    food_preferences: Optional[FoodPreferences] = Field(None, description="그룹의 통합 음식 선호도")
    play_preferences: Optional[PlayPreferences] = Field(None, description="그룹의 통합 놀이 선호도")

class GroupList(BaseModel):
    groups: List[GroupResponse]

class Message(BaseModel):
    message: str
