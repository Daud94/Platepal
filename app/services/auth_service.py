from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from pydantic.v1.parse import load_file
from rich import panel

from app.config import settings
from app.core.security import oauth2_scheme
from app.core.utils import hash_password, verify_password, create_access_token, verify_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUser, LoginUser


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def signup(self, payload: CreateUser):
        existing_user = await self.user_repo.get_user({"email": payload.email})
        print(existing_user)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        payload.password = hash_password(payload.password)
        payload.user_type = payload.user_type
        await self.user_repo.create_user(payload)

    async def get_current_user(self, token:Annotated[str, Depends(oauth2_scheme)]) -> User:
        payload = verify_access_token(token)
        user = await self.user_repo.get_user(where={"id": payload["userId"]})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return user

    async def login(self, username: str, password: str) -> str:
        user = await self.user_repo.get_user(where={"email": username})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

        is_match = verify_password(password, user.password)
        if not is_match:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")

        access_token = create_access_token(data={"userId": user.id, "user_type": user.user_type},
                                           expires_delta=timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
        return access_token
