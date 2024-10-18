from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
import datetime

# Configuration
SECRET_KEY = "your_secret_key"  # Secret key for encoding the JWT token
ALGORITHM = "HS256"  # Algorithm used for encoding the JWT token

# Create a FastAPI application
app = FastAPI()

# Create OAuth2PasswordBearer to extract the token from the header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to create a JWT token
def create_jwt_token(data: dict):
    # Set expiration time for the token (30 minutes from now)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data.update({"exp": expiration})  # Add expiration time to the payload
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)  # Encode the JWT token

# Stub function for checking user credentials
def authenticate_user(username: str, password: str) -> bool:
    # Assume we have a database of users
    valid_users = [
        {"username": "john_doe", "password": "adminpass"},  # Valid user example
        {"username": "securepassword123", "password": "userpass"}  # Another valid user
    ]
    
    # Check for matching username and password
    for user in valid_users:
        if user["username"] == username and user["password"] == password:
            return True  # Credentials are valid
    return False  # Credentials are invalid

# Function to verify the JWT token
def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token to retrieve the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the payload if the token is valid
    except jwt.ExpiredSignatureError:
        # Handle case when the token has expired
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        # Handle case when the token is invalid
        raise HTTPException(status_code=401, detail="Invalid token")

# Model for incoming user data
class User(BaseModel):
    username: str  # Username field
    password: str  # Password field

@app.post("/login")
async def login(user_in: User):
    # Check user credentials using the authenticate_user function
    if authenticate_user(user_in.username, user_in.password):
        # If credentials are valid, create and return a JWT token
        return {
            "access_token": create_jwt_token({"sub": user_in.username}),  # Create token with username as subject
            "token_type": "bearer"  # Indicate token type
        }
    # If credentials are invalid, raise an HTTP exception with a 401 status
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/protected_resource")
async def protected_resource(token: str = Depends(verify_jwt_token)):
    # This endpoint is protected; only accessible with a valid token
    return {"message": "This is a protected resource!", "user": token["sub"]}  # Return a message and the username
