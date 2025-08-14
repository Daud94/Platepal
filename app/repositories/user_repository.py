from typing import Any
from uuid import UUID

from app.config.database import sessionDep
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.auth_schema import CreateUser


class UserRepository(BaseRepository):
    def __init__(self, session: sessionDep):
        super().__init__(session, User)

    async def create(self, payload: CreateUser):
        await self._create(payload.model_dump())

    async def get_by_id(self, id: UUID):
        return await self._get_by_id(id)

    async def get(self, where: dict):
        print("where", where)
        return await self._get(where)
