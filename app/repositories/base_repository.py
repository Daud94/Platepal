from typing import Any, TypeVar
from uuid import UUID

from sqlmodel import SQLModel, select

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T', bound=SQLModel)


class BaseRepository:
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def _create(self, payload: dict[str, Any]) -> T:
        """Create a new instance of the model.

        Args:
            payload: Dictionary containing model field values

        Returns:
            The created model instance
        """
        instance = self.model(**payload)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def _get_by_id(self, id: UUID) -> T | None:
        """Retrieve a model instance by its ID.

        Args:
            id: UUID of the instance to retrieve

        Returns:
            The model instance if found, None otherwise
        """
        return await self.session.get(self.model, id)

    async def _get(self, where: dict) -> T | None:
        """Retrieve a model instance by filter conditions.

        Args:
            where: Dictionary of filter conditions

        Returns:
            The first matching model instance if found, None otherwise
        """
        result = await self.session.execute(
            select(self.model).filter_by(**where)
        )
        return result.scalars().first()
