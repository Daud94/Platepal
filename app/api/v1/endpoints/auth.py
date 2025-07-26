from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.utils import status_code_ranges
from starlette.responses import JSONResponse

from app.dependencies import get_auth_service
from app.schemas.user_schema import CreateUser
from app.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
)


@router.post('/signup')
def signup(payload: CreateUser, auth_service: AuthService = Depends(get_auth_service)):
    auth_service.signup(payload)
    return JSONResponse(status_code=201, content={"success": True, "message": "Signup successful"})
