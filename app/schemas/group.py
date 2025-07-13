from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.group import GroupModel
import datetime

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
    pass

class GroupList(BaseModel):
    groups: List[GroupResponse]

class Message(BaseModel):
    message: str
