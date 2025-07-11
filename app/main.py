from fastapi import FastAPI
from .db import client, database

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = database

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to PlayFriends API"}
