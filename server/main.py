from fastapi import FastAPI
from routers import auth, users, websockets

from openai import OpenAI
import os
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


class Context(BaseModel):
    audio_content: str
    context: str
@app.post("/summarize")
async def summarize(context: Context):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Given the context, which is: {context.context}, please provide a concise summary of the main points, with title and bulletpoints if needed, and from the following audio content: {context.audio_content}"
    model="gpt-3.5-turbo-1106"
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    print(response.choices)
    return response.choices[0].message.content