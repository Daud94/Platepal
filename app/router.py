from app.api.v1.endpoints import auth, user
from app.config import settings
from fastapi import APIRouter

router = APIRouter()


router.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
router.include_router(user.router, prefix=settings.API_V1_STR, tags=["Users"])