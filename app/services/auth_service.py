from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.security import verify_password
from app.models.user import UserModel

async def authenticate_user(db: AsyncIOMotorDatabase, userid: str, password: str) -> Optional[UserModel]:
    user = await db.users.find_one({"userid": userid})
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
        
    return UserModel(**user)
