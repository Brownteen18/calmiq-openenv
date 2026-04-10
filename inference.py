from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()

# Env variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

# Safe OpenAI client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else None
)

@app.get("/")
def root():
    return {"message": "Server is running successfully 🚀"}

@app.post("/reset")
async def reset():
    return {"status": "reset done"}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()

        messages = body.get("messages", [])

        # Fallback if no API
        if OPENAI_API_KEY == "dummy":
            return {
                "choices": [
                    {
                        "message": {
                            "content": "This is a dummy response"
                        }
                    }
                ]
            }

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages
        )

        return JSONResponse(content=response.model_dump())

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
