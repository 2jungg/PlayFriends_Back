from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DATABASE: str
    GEMINI_API_KEY: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
