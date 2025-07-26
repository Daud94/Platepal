from app.database import sessionDep
from app.repositories.user_repository import UserRepository
from fastapi import Depends

from app.services.auth_service import AuthService


def get_user_repository(session: sessionDep) -> UserRepository:
    return UserRepository(session=session)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserRepository:
    return AuthService(user_repo=user_repo)
