from fastapi.openapi.models import EmailStr
from pydantic import BaseModel

from app.enums.user_type import UserType
from app.schemas.base_response_schema import BaseResponse


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    user_type: UserType

class Token(BaseModel):
    access_token: str
    token_type: str

class SignupResponse(BaseResponse):
    pass

class LogoutResponse(BaseResponse):
    pass