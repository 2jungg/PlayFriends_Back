from fastapi import FastAPI
from app.db.session import client
from app.api.routers import example, users

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = client.get_database("mydatabase")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(example.router, tags=["example"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
