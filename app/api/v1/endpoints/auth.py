from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.dependencies import get_auth_service
from app.schemas.responses_schema import LoginUserResponse
from app.schemas.user_schema import CreateUser, LoginUser
from app.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
)


@router.post('/signup')
def signup(payload: CreateUser, auth_service: AuthService = Depends(get_auth_service)):
    auth_service.signup(payload)
    return JSONResponse(status_code=201, content={"success": True, "message": "Signup successful"})


@router.post('/login', response_model=LoginUserResponse)
def login(payload: LoginUser, auth_service: AuthService = Depends(get_auth_service)):
    access_token = auth_service.login(payload)
    return LoginUserResponse(
        success=True,
        message="Login successful",
        auth_token=access_token
    )
