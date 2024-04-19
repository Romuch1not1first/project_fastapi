from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models.models import User

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/user")
def create_user(user: User):
    is_adult = user.age >= 18
    user_data = user.dict()
    user_data["is_adult"] = is_adult
    return JSONResponse(content=user_data)