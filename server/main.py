from fastapi import FastAPI, WebSocket
from routers import auth, users, websockets
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI()
app.include_router(websockets.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello"}