from pydantic import BaseModel


class LoginUserResponse(BaseModel):
    success: bool
    message: str
    token: str