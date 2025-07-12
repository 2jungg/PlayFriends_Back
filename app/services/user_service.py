from sqlalchemy.orm import Session
from repositories.user_repository import create_user, get_user_by_username
from schemas.user import UserCreate, UserResponse

def register_user(db: Session, user_create: UserCreate) -> UserResponse:
    existing_user = get_user_by_username(db, user_create.username)
    if existing_user:
        raise ValueError("Username already exists")
    
    user = create_user(db, user_create)
    return UserResponse.model_validate(user)