from pydantic import BaseModel, Field
from datetime import datetime

class ActivityLogModel(BaseModel):
    id: str = Field(alias="_id", default=None)
    user_id: str = Field(..., description="UserModel의 ID")
    group_id: str = Field(..., description="GroupModel의 ID")
    activity_id: str = Field(..., description="ActivityModel의 ID")
    rating: int = Field(..., ge=1, le=5, description="사용자가 매긴 평점 (1-5)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {"id": str}
