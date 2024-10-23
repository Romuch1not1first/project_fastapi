from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from time import time

app = FastAPI()

# In-memory storage for users
users_db = {"user1": {"username": "user1", "email": "user1@example.com", "age": 30}}

# Error response model using Pydantic
class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: str


# Custom exception for user not found
class UserNotFoundException(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(
            status_code=404,
            detail=f"User with ID '{user_id}' not found",
            headers={"X-Error": "User Not Found"},
        )


# Custom exception for invalid user data
class InvalidUserDataException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=message,
            headers={"X-Error": "Invalid User Data"},
        )


# Exception handler for UserNotFoundException
@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    start_time = time()
    error_response = ErrorResponseModel(
        status_code=exc.status_code, message=exc.detail, error_code="USER_NOT_FOUND"
    )
    end_time = time()
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(),
        headers={"X-ErrorHandleTime": f"{end_time - start_time:.4f} seconds"},
    )


# Exception handler for InvalidUserDataException
@app.exception_handler(InvalidUserDataException)
async def invalid_user_data_exception_handler(
    request: Request, exc: InvalidUserDataException
):
    start_time = time()
    error_response = ErrorResponseModel(
        status_code=exc.status_code, message=exc.detail, error_code="INVALID_USER_DATA"
    )
    end_time = time()
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(),
        headers={"X-ErrorHandleTime": f"{end_time - start_time:.4f} seconds"},
    )


# User registration model
class UserRegistrationModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(..., ge=18)
    password: str = Field(..., min_length=8, max_length=16)
    phone: Optional[str] = None


# Route for user registration
@app.post("/register/")
async def register_user(user: UserRegistrationModel):
    if user.username in users_db:
        raise InvalidUserDataException(f"User '{user.username}' already exists.")
    users_db[user.username] = user.dict()
    return {"message": "User registered successfully", "user": user.dict()}


# Route to retrieve user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    if user_id not in users_db:
        raise UserNotFoundException(user_id)
    return {"user": users_db[user_id]}
