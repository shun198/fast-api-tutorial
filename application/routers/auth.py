from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/api/auth")
async def get_user():
    return {"user": "authenticate"}
