from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.dependencies import get_auth_service, get_current_user
from app.models.user import User


router = APIRouter(
    prefix='/users',
)

auth_service = get_auth_service()

@router.get('/profile')
def get_user_profile(current_user: Annotated[User, Depends(get_current_user)],):
    user = current_user
    return {
        "success": True,
        "message": "User profile retrieved successfully",
        "data": {
            "id": user.id,
            "email": user.email,
            "user_type": user.user_type
        }
    }
