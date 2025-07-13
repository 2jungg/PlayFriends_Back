from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
from bson import ObjectId
import datetime

class GroupModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    groupname: str = Field(..., description="그룹 이름")
    starttime: datetime.datetime = Field(..., description="시작 시간")
    endtime: Optional[datetime.datetime] = Field(None, description="종료 시간")
    is_active: bool = Field(True)
    owner_id: str = Field(..., description="방장 _ID")
    member_ids: List[str] = Field(default=[], description="참여자 _ID 목록")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime.datetime: lambda dt: dt.isoformat(),
        }
