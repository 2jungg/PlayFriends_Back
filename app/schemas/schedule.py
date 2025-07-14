from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
from app.models.activity import GeoJson

class ScheduledActivity(BaseModel):
    name: str = Field(..., description="활동의 이름")
    category: str = Field(..., description="카테고리 이름")
    start_time: datetime.datetime = Field(..., description="활동 시작 시간")
    end_time: datetime.datetime = Field(..., description="활동 종료 시간")
    location: Optional[GeoJson] = Field(None, description="활동 장소")

    class Config:
        from_attributes = True

class ScheduleSuggestion(BaseModel):
    group_id: str = Field(..., description="그룹의 ID")
    scheduled_activities: List[ScheduledActivity] = Field(..., description="스케줄된 활동 목록")

class ListScheduleResponse(BaseModel):
    schedules: List[ScheduleSuggestion]
