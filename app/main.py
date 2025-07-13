from fastapi import FastAPI
from app.api.routers import example, users, groups
from app.core.config import settings
from app.db.session import client

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = client[settings.MONGO_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(example.router, tags=["example"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(groups.router, prefix="/api/v1", tags=["groups"])
