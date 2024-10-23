# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Словарь для хранения пользователей
users_db = {}

class User(BaseModel):
    username: str
    email: str

@app.post("/register/", response_model=User)
async def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already registered")
    users_db[user.username] = user
    return user

@app.get("/users/{username}", response_model=User)
async def get_user(username: str):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{username}", response_model=dict)
async def delete_user(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[username]
    return {"detail": "User deleted"}
