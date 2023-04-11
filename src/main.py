"""Simple FastAPI and Redis server"""
from fastapi import FastAPI
from fastapi import HTTPException
import redis
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    phone: str
    address: str

redis_db = redis.Redis(host='localhost', port=6379, db=0)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.post("/write_data")
async def write_data(data: Data):
    redis_db.set(data.phone, data.address)
    return {"message": "Data written successfully"}

@app.get("/check_data")
async def check_data(phone: str):
    address = redis_db.get(phone)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"phone": phone, "address": address.decode()}

@app.put("/write_data")
async def update_data(data: Data):
    if redis_db.get(data.phone) is None:
        raise HTTPException(status_code=404, detail="Data not found")
    redis_db.set(data.phone, data.address)
    return {"message": "Data updated successfully"}
