from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.db.session import client, database

router = APIRouter()

# Dependency to get the database client and database
def get_db_client() -> AsyncIOMotorClient:
    return client

def get_db() -> AsyncIOMotorDatabase:
    return database

@router.get("/")
def read_root():
    return {"message": "Welcome to PlayFriends API"}

@router.get("/number/{number}")
def read_number(number: int):
    return {"number": number}

@router.get("/database")
def get_database_info(db: AsyncIOMotorDatabase = Depends(get_db), db_client: AsyncIOMotorClient = Depends(get_db_client)):
    return {"database_name": db.name, "client_address": str(db_client.address)}
