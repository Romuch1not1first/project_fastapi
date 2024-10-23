# app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/sum/")
async def calculate_sum(a: int, b: int):
    return {"result": a + b}
