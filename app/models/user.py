from sqlmodel import SQLModel, Field

from app.enums.user_type import UserType

class User(SQLModel, table=True):
    __name__ = "users"
    id: int = Field(primary_key=True, unique=True, index=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    password: str
    user_type: UserType

