from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
from bson import ObjectId
import datetime
from app.schemas.user import FoodPreferences, PlayPreferences
from app.schemas.schedule import ScheduledActivity

class GroupModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    groupname: str = Field(..., description="그룹 이름")
    starttime: datetime.datetime = Field(..., description="시작 시간")
    endtime: Optional[datetime.datetime] = Field(None, description="종료 시간")
    is_active: bool = Field(True)
    owner_id: str = Field(..., description="방장 _ID")
    member_ids: List[str] = Field(default=[], description="참여자 _ID 목록")

    food_preferences: Optional[FoodPreferences] = Field(None, description="그룹의 통합 음식 선호도")
    play_preferences: Optional[PlayPreferences] = Field(None, description="그룹의 통합 놀이 선호도")

    schedule: Optional[List[ScheduledActivity]] = Field(None, description="확정된 스케줄")
    distances_km: Optional[List[float]] = Field(None, description="스케줄 장소 간 이동 거리 목록 (km)")

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
