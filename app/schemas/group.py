from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.group import GroupModel
import datetime
from .user import FoodPreferences, PlayPreferences
from .schedule import ScheduledActivity

class GroupCreate(BaseModel):
    groupname: str
    starttime: datetime.datetime
    endtime: Optional[datetime.datetime]

class GroupUpdate(BaseModel):
    groupname: Optional[str] = None
    starttime: Optional[datetime.datetime] = None
    endtime: Optional[datetime.datetime] = None
    is_active: Optional[bool] = None
    food_preferences: Optional[FoodPreferences] = None
    play_preferences: Optional[PlayPreferences] = None
    member_ids: Optional[List[str]] = None
    schedule: Optional[List[ScheduledActivity]] = None
    distances_km: Optional[List[float]] = None

class GroupMember(BaseModel):
    id: str
    name: str

class GroupDetailResponse(GroupModel):
    members: List[GroupMember] = Field([], description="참여자 이름 목록")

class GroupList(BaseModel):
    groups: List[GroupDetailResponse]

class Message(BaseModel):
    message: str
