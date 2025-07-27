from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
import jwt
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.core.utils import hash_password, verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUser, LoginUser


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def signup(self, payload: CreateUser):
        existing_user = self.user_repo.get_user(where={"email": payload.email})
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        payload.password = hash_password(payload.password)
        payload.user_type = payload.user_type
        self.user_repo.create_user(payload)

    def login(self, payload: LoginUser) -> str:
        user = self.user_repo.get_user(where={"email": payload.email})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

        is_match = verify_password(payload.password, user.password)
        if not is_match:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")

        access_token = create_access_token(data={"userId": user.id},
                                           expires_delta=timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
        return access_token
