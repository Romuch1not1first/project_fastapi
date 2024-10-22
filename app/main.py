from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for formatting error responses
class ErrorResponseModel(BaseModel):
    code: int
    message: str
    details: str


# Custom exception A for specific error scenarios
class CustomExceptionA(Exception):
    def __init__(self, detail: str):
        self.detail = detail


# Custom exception B for different error scenarios
class CustomExceptionB(Exception):
    def __init__(self, detail: str):
        self.detail = detail


# Exception handler for CustomExceptionA
# Returns a JSON response with a 400 status code and custom error message
@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=400,
        content=ErrorResponseModel(
            code=400, 
            message="Custom Error A Occurred", 
            details=exc.detail
        ).dict()
    )


# Exception handler for CustomExceptionB
# Returns a JSON response with a 404 status code and custom error message
@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=404,
        content=ErrorResponseModel(
            code=404, 
            message="Custom Error B Occurred", 
            details=exc.detail
        ).dict()
    )


# First endpoint that raises CustomExceptionA when value < 10
# Triggers a 400 error if the condition is met
@app.get("/endpoint_a/")
async def trigger_custom_exception_a(value: int):
    if value < 10:
        raise CustomExceptionA(detail="Value is too small")
    return {"message": "Value is acceptable"}


# Second endpoint that raises CustomExceptionB when item_id == 42
# Triggers a 404 error if the condition is met
@app.get("/endpoint_b/{item_id}/")
async def trigger_custom_exception_b(item_id: int):
    if item_id == 42:
        raise CustomExceptionB(detail="Item with ID 42 not found")
    return {"item_id": item_id}
