from typing import Annotated

from app.database import sessionDep
from app.models.user import User
from app.repositories.user_repository import UserRepository
from fastapi import Depends
from app.core.security import oauth2_scheme

from app.services.auth_service import AuthService


def get_user_repository(session = sessionDep) -> UserRepository:
    return UserRepository(session=session)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo=user_repo)


async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)],
                     auth_service: AuthService = Depends(get_auth_service)) -> User:
    return await auth_service.get_current_user(token=token)
