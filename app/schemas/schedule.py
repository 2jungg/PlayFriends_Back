from pydantic import BaseModel, Field
from typing import List
import datetime
from app.models.schedule import ScheduledActivity

class ScheduleResponse(BaseModel):
    id: str
    group_id: str
    scheduled_activities: List[ScheduledActivity]
    created_at: datetime.datetime

    class Config:
        from_attributes = True
