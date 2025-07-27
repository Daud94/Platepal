from pydantic import BaseModel, EmailStr, Field

from app.enums.user_type import UserType


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    user_type: UserType

class LoginUser(BaseModel):
    email: EmailStr
    password: str

