from typing import Annotated

from app.database import sessionDep
from app.models.user import User
from app.repositories.user_repository import UserRepository
from fastapi import Depends, Header

from app.services.auth_service import AuthService


def get_user_repository(session: sessionDep) -> UserRepository:
    return UserRepository(session=session)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserRepository:
    return AuthService(user_repo=user_repo)


def get_current_user(authorization: Annotated[str, Header()], auth_service: AuthService = Depends(get_auth_service)) -> User:
    return auth_service.get_current_user(authorization=authorization)  # Assuming authorization is passed as a header dependency