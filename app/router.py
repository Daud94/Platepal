from app.api.v1.endpoints import auth, user
from fastapi import APIRouter

from app.config.env_config import settings

router = APIRouter()


router.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
router.include_router(user.router, prefix=settings.API_V1_STR, tags=["Users"])