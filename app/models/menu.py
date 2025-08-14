from uuid import uuid4, UUID
from sqlalchemy import Column, NUMERIC
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship


class Menu(SQLModel, table=True):
    __tablename__ = "menus"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    category: str
    name: str
    image: str
    description: str
    ingredients: list[str] = Field(sa_column=Column(JSONB))
    price: float = Field(default=0.0, sa_column=Column(NUMERIC(10, 2)))
    price_description: str

    user_id: UUID = Field(foreign_key="users.id", index=True)
    user: "User" = Relationship(
        back_populates="menus",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
