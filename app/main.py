from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from starlette.responses import Response

app = FastAPI()

# Initialize the dependency for base auntification
security = HTTPBasic()

# Credentials database
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# Function to check credentials
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == VALID_USERNAME
    correct_password = credentials.password == VALID_PASSWORD

    if not (correct_username and correct_password):
        # If the data is incorrect, you get error 401 and add title WWW-Authenticate
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.get("/secret")
def get_secret_message(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    # If the data is correct, return a secret message
    return {"message": "You got my secret, welcome"}
