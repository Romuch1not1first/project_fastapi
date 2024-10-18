from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/headers")
def get_headers(request: Request):
    # Извлечение заголовков
    user_agent = request.headers.get("user-agent")
    accept_language = request.headers.get("accept-language")

    # Проверка на наличие заголовков
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Missing required headers: 'User-Agent' or 'Accept-Language'")
    
    # Возврат значений заголовков в ответе
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }
