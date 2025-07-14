from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
from bson import ObjectId
import datetime
from bson import ObjectId

class ScheduledActivity(BaseModel):
    activity_id: str = Field(..., description="활동의 ID")
    start_time: datetime.datetime = Field(..., description="활동 시작 시간")
    end_time: datetime.datetime = Field(..., description="활동 종료 시간")

class ScheduleModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    group_id: str = Field(..., description="그룹의 ID")
    scheduled_activities: List[ScheduledActivity] = Field(..., description="스케줄된 활동 목록")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, description="생성 시간")

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

class ListScheduleModel(BaseModel):
    schedules: List[ScheduleModel]