from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, conint, constr
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Pydantic model for validating user data
class User(BaseModel):
    username: str  # Simple string for username
    age: conint(gt=18)  # Age must be greater than 18 (conint is an integer with constraints)
    email: EmailStr  # Built-in validation for proper email format
    password: constr(min_length=8, max_length=16)  # Password must be between 8-16 characters
    phone: Optional[str] = 'Unknown'  # Optional phone number, default value is 'Unknown'

# Custom exception handler for validation errors
# Handles validation errors (e.g., wrong types, missing fields) and returns a 422 response with error details
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

# API endpoint for user registration
# This endpoint validates the incoming JSON payload against the User model
@app.post("/register/")
async def register_user(user: User):
    return {"message": "User registered successfully", "user": user}
