from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.dependencies import get_auth_service
from app.schemas.responses_schema import LoginUserResponse
from app.schemas.token_schema import Token
from app.schemas.user_schema import CreateUser, LoginUser
from app.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
)


@router.post('/signup')
async def signup(payload: CreateUser, auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.signup(payload=payload)
    return JSONResponse(status_code=201, content={"success": True, "message": "Signup successful"})


@router.post('/login', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                auth_service=Depends(get_auth_service)):
    access_token = await auth_service.login(username=form_data.username, password=form_data.password)
    return Token(access_token=access_token, token_type="bearer")
