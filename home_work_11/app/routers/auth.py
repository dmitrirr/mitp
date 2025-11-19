from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_auth_service
from ..models.users import TokenResponse, UserLoginRequest, UserRegisterRequest
from ..service.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(
    user: UserRegisterRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        token = service.register(user.email, user.password)
        return TokenResponse(token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    user: UserLoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        token = service.login(user.email, user.password)
        return TokenResponse(token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/signout")
async def signout():
    # including this to satisfy home work requirements
    return {"message": "Signed out"}

