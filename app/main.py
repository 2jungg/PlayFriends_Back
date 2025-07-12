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

@app.get("/number/{number}")
def read_number(number: int):
    return {"number": number}

@app.get("/database")
def get_database_info():
    return {"database_name": app.mongodb.name, "client_address": str(app.mongodb_client.address)}
