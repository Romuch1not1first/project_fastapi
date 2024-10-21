from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# PostgreSQL database URL (replace 'user', 'password', 'localhost', and 'dbname' with your actual PostgreSQL credentials)
DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Create an instance of the Database object. This will handle the connection and interaction with the PostgreSQL database.
# The Database class from the 'databases' library allows asynchronous queries, which is helpful for high-performance applications.
database = Database(DATABASE_URL)

# Pydantic model for incoming user data validation
# This model will validate the data received from the client in the request body (e.g., for creating a new user).
class UserCreate(BaseModel):
    username: str  # This field will accept the username as a string
    email: str     # This field will accept the email as a string

# Pydantic model for returning user data to the client
# This is used to format the response after a user is successfully created.
class UserReturn(BaseModel):
    username: str  # This field will return the username
    email: str     # This field will return the email
    id: Optional[int] = None  # Optional field to return the user's ID from the database after creation

# Event handler that will run when the application starts
# It ensures the connection to the database is established before processing any requests.
@app.on_event("startup")
async def startup_database():
    await database.connect()  # Connect to the PostgreSQL database when the FastAPI application starts

# Event handler that will run when the application is shutting down
# This ensures that the connection to the database is properly closed to avoid any resource leakage.
@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()  # Disconnect from the PostgreSQL database when the FastAPI application stops

# Create a route to handle POST requests for creating new users
# The response_model argument specifies that the output should conform to the UserReturn schema.
@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    # SQL query to insert a new user into the 'users' table
    # The values ':username' and ':email' are placeholders that will be replaced with actual data from the request
    query = "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    
    # A dictionary containing the actual values that will replace the placeholders in the query
    values = {"username": user.username, "email": user.email}
    
    try:
        # Execute the SQL query asynchronously and retrieve the new user's ID
        # The 'execute' method runs the query and returns the value of the 'RETURNING' clause (in this case, the ID)
        user_id = await database.execute(query=query, values=values)
        
        # Return the newly created user's data, including the ID
        # user.dict() returns the username and email fields as a dictionary, and we add the 'id' to the response
        return {**user.dict(), "id": user_id}
    
    except Exception as e:
        # If there is an error during the query execution, raise an HTTPException with a 500 status code
        # This will notify the client that something went wrong on the server.
        raise HTTPException(status_code=500, detail="Failed to create user")
