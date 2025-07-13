from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from app.db.session import get_db
from app.schemas.user import User, UserCreate, Token
from app.schemas.group import GroupList
from app.models.user import UserModel
from app.core.security import create_access_token, get_current_user
from app.services.auth_service import authenticate_user
from app.services.user_service import UserService
from app.core.config import settings
from datetime import timedelta
from app.schemas.user import LoginRequest

router = APIRouter()

def get_user_service(db: AsyncIOMotorClient = Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: LoginRequest,
    db: AsyncIOMotorClient = Depends(get_db)
):
    user = await authenticate_user(db[settings.MONGO_DATABASE], form_data.userid, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 자동 로그인 여부에 따라 만료 시간 설정
    if form_data.auto_login:
        expires_delta = timedelta(days=30) # 30일
    else:
        expires_delta = timedelta(minutes=30) # 30분

    access_token = create_access_token(
        data={"sub": user.userid}, expires_delta=expires_delta
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: UserModel = Depends(get_current_user)):
    # In a real application, you would invalidate the token.
    # For simplicity, we'll just return a success message.
    return {"message": "Successfully logged out"}

@router.post("/create_user/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """
    Create a new user.
    """
    existing_user = await service.get_user_by_userid(user_in.userid)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this userid already exists in the system.",
        )
    
    new_user = await service.create_user(user_in)
    return new_user

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return User(**current_user.model_dump(by_alias=True))

@router.get("/users/{user_id}/groups", response_model=GroupList)
async def get_groups_by_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    if current_user.userid != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's groups",
        )

    user = await service.get_user_by_userid(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    groups = await service.get_user_groups(user)
    return {"groups": groups}
