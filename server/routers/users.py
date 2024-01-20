from fastapi import APIRouter

user_router = APIRouter()


@user_router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@user_router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@user_router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}