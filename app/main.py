from fastapi import FastAPI, Form, Request, Response, status
from fastapi.responses import JSONResponse
import uuid

app = FastAPI()

# Условные данные для авторизации и сессий
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"
session_tokens = {}  # Храним активные токены сессий

@app.post("/login")
async def login(
    username: str = Form(...),  # Используем Form для передачи данных формы
    password: str = Form(...),  # Используем Form для передачи данных формы
    response: Response = None
):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session_token = str(uuid.uuid4())
        session_tokens[session_token] = {"username": username}  # Сохраняем токен в памяти
        response.set_cookie(key="session_token", value=session_token, httponly=True, secure=False)  # secure=False для локального тестирования
        return JSONResponse(content={"message": "Logged in successfully!"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"error": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/user")
async def get_user_profile(request: Request):
    # Получаем session_token из cookie
    session_token = request.cookies.get("session_token")
    
    # Проверяем, предоставлен ли токен
    if not session_token:
        return JSONResponse(content={"message": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    # Проверяем, есть ли токен в нашем "хранилище"
    user_session = session_tokens.get(session_token)
    
    # Если токен недействителен
    if not user_session:
        return JSONResponse(content={"message": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    # Возвращаем профиль пользователя
    return JSONResponse(content={"username": user_session["username"], "profile": "This is your profile info!"}, status_code=status.HTTP_200_OK)