from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

class ActivityModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    name: str = Field(..., description="활동 이름")
    description: Optional[str] = Field(None, description="활동 설명")
    location: Optional[str] = Field(None, description="활동 장소")
    time: datetime.datetime = Field(..., description="활동 시간")
    
    group_id: str = Field(..., description="이 활동을 생성한 Group ID")
    category_id: str = Field(..., description="이 활동이 속한 Category ID")
    participant_ids: List[str] = Field(default=[], description="참여자 User ID 목록")

    class Config:
        from_attributes = True
        validate_by_name = True
        json_encoders = {
            "id": str,
            "time": lambda dt: dt.isoformat()
        }
