from fastapi import Depends, HTTPException, status

from app.core.utils import hash_password
from app.database import get_session, sessionDep
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUser

session = Depends(get_session)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def signup(self, payload: CreateUser):
        existing_user = self.user_repo.get_user(where={"email": payload.email})
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        payload.password = hash_password(payload.password)
        self.user_repo.create_user(payload)
