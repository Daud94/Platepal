from datetime import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from app.enums.user_type import UserType
from app.models.menu import Menu
from sqlalchemy.dialects import postgresql


class User(SQLModel, table=True):
	__tablename__ = "users"
	id: UUID = Field(
		sa_column=Column(
			postgresql.UUID,
			default=uuid4,
			primary_key=True,
		)
	)
	first_name: str
	last_name: str
	email: EmailStr = Field(unique=True, index=True)
	password: str
	user_type: UserType
	email_verified: bool = Field(default=False, nullable=False)
	email_token: str | None = Field(default=None, nullable=True)
	otp_expiration: datetime | None = Field(default=None, nullable=True)
	menus: list[Menu] = Relationship(
		back_populates="user",
		sa_relationship_kwargs={"lazy": "selectin"},
	)
