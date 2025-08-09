from typing import Annotated

from app.config.database import sessionDep
from app.config.redis import is_jti_blacklisted
from app.core.utils import verify_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from fastapi import Depends, HTTPException, status
from app.core.security import oauth2_scheme

from app.services.auth_service import AuthService


def get_user_repository(session=sessionDep) -> UserRepository:
    return UserRepository(session=session)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo=user_repo)


async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    token_data = verify_access_token(token)
    if await is_jti_blacklisted(token_data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return token_data


async def get_current_user(token_data: Annotated[dict, Depends(get_access_token)],
                           auth_service: AuthService = Depends(get_auth_service)) -> User:
    return await auth_service.get_current_user(token_data)
