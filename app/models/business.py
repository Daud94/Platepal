from uuid import uuid4, UUID

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import SQLModel, Field


class Business(SQLModel, table=True):
    __tablename__ = 'businesses'
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
