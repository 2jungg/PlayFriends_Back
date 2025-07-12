from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.session import database
from app.schemas.user import User, UserCreate, FoodPreferences, ActivityPreferences
from app.models.user import UserModel

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(lambda: database)):
    """
    Create a new user.
    """
    existing_user = await db.users.find_one({"userid": user_in.userid})
    if existing_user:
        if existing_user["userid"] == user_in.userid:
            detail = "The user with this userid already exists in the system."
        else:
            detail = "The user with this username already exists in the system."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    
    hashed_password = get_password_hash(user_in.password)
    user_dict = user_in.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]

    # Add default preferences and log
    user_dict.update({
        "food_preferences": FoodPreferences().dict(),
        "activity_preferences": ActivityPreferences().dict(),
        "activity_log": []
    })
    
    # Create user in the database
    new_user = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": new_user.inserted_id})

    # Manually convert ObjectId to string for the response
    if created_user and "_id" in created_user:
        created_user["_id"] = str(created_user["_id"])

    return created_user
