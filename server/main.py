from fastapi import FastAPI
from routers import users, websockets

app = FastAPI()
app.include_router(users.user_router)
app.include_router(websockets.ws_router)

@app.get("/")
async def root():
    return {"message": "Hello"}