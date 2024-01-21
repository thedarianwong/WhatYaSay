from fastapi import FastAPI, WebSocket
from routers import auth, users, websockets

from openai import OpenAI
import os
import pandas as pd
import time
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

app = FastAPI()
app.include_router(websockets.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello"}


class AudioContent(BaseModel):
    audio_content: str
@app.post("/summarize")
async def summarize(audio_content: AudioContent):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Summarize main points for me: {audio_content}"
    model="gpt-3.5-turbo"
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message["content"]