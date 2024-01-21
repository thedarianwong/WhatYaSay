from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])  # Added prefix here


@router.get("/", tags=["auth"])
async def test():
    return [{"username": "sbs"}, {"username": "Morty"}]
