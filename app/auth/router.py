from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import jwt, service
from app.auth.schemas import AccessTokenResponse, JWTData, LoginDto, RegisterDto
from app.database import db_deps
from app.users.schemas import UserDto

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserDto)
async def register(data: RegisterDto, db: db_deps):
    return await service.register(db, data)


@auth_router.post("/login", response_model=AccessTokenResponse)
async def login(
    db: db_deps,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    user = await service.login(
        db, LoginDto(username=form_data.username, password=form_data.password)
    )
    return AccessTokenResponse(access_token=jwt.create_access_token(user))


@auth_router.get("/me", response_model=UserDto)
async def get_current_user(
    db: db_deps, jwt_data: Annotated[JWTData, Depends(jwt.parse_jwt_user_data)]
):
    user = await service.get_user_by_username(db, jwt_data.username)
    return user
