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
    member_ids: Optional[List[str]] = None
    schedule: Optional[List[ScheduledActivity]] = None
    distances_km: Optional[List[float]] = None

class GroupResponse(GroupModel):
    food_preferences: Optional[FoodPreferences] = Field(None, description="그룹의 통합 음식 선호도")
    play_preferences: Optional[PlayPreferences] = Field(None, description="그룹의 통합 놀이 선호도")

class GroupMember(BaseModel):
    id: str
    name: str

class GroupDetailResponse(GroupResponse):
    members: List[GroupMember] = Field([], description="참여자 이름 목록")
    schedule: Optional[List[ScheduledActivity]] = Field(None, description="확정된 스케줄")
    distances_km: Optional[List[float]] = Field(None, description="스케줄 장소 간 이동 거리 목록 (km)")

class GroupList(BaseModel):
    groups: List[GroupDetailResponse]

class Message(BaseModel):
    message: str
