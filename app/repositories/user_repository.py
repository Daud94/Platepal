from typing import Any
from uuid import UUID

from app.config.database import sessionDep
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.auth_schema import CreateUser


class UserRepository(BaseRepository):
	def __init__(self, session: sessionDep):
		super().__init__(session, User)

	async def create(self, payload: CreateUser) -> User:
		user = await self._create(payload.model_dump())
		return user

	async def get_by_id(self, id: UUID) -> User | None:
		user = await self._get_by_id(id)
		return user

	async def get(self, where: dict) -> User | None:
		user = await self._get(where)
		return user

	async def update(self, id: UUID, payload: dict[str, Any]) -> User:
		user = await self._update(id, payload)
		return user
