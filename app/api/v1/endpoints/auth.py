from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.config.redis import add_jti_to_blacklist
from app.dependencies import get_auth_service, get_access_token

from app.schemas.auth_schema import SignupResponse, Token, CreateUser, LogoutResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
)



@router.post('/signup', response_model=SignupResponse)
async def signup(payload: CreateUser, auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.signup(payload=payload)
    return {
        "success": True,
        "message": "Signup successful"
    }


@router.post('/login', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                auth_service=Depends(get_auth_service)):
    access_token = await auth_service.login(username=form_data.username, password=form_data.password)
    return Token(token=access_token, access_token="bearer")


@router.get('/logout', response_model=LogoutResponse)
async def logout(token_data: Annotated[dict, Depends(get_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {
        "success": True,
        "message": "Logout successful"
    }



