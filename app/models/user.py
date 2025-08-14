from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from app.enums.user_type import UserType
from app.models.menu import Menu
from sqlalchemy.dialects import postgresql


class User(SQLModel, table=True):
    __tablename__ = "users"
    # id: int = Field(primary_key=True, unique=True, index=True)
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)
    password: str
    user_type: UserType

    menus: list[Menu] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
