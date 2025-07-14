from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.api.routers import example, users, groups
from app.core.config import settings
from app.db.session import client
from app.services.group_service import GroupService

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = client
    app.mongodb = client[settings.MONGO_DATABASE]
    
    group_service = GroupService(app.mongodb_client)
    scheduler.add_job(group_service.deactivate_expired_groups, 'cron', hour=0)
    scheduler.start()
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(example.router, tags=["example"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(groups.router, prefix="/api/v1", tags=["groups"])
