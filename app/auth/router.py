from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import jwt, service, utils
from app.auth.dependencies import valid_refresh_token, valid_refresh_token_user
from app.auth.models import RefreshToken, User
from app.auth.schemas import (
    AccessTokenResponse,
    JWTData,
    LoginDto,
    RegisterDto,
    UserDto,
)
from app.auth.utils import get_refresh_token_cookie_settings
from app.database import db_deps

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
    refresh_token = await jwt.create_refresh_token(db, user.id)

    response.set_cookie(**get_refresh_token_cookie_settings(refresh_token))
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user), refresh_token=refresh_token
    )


@auth_router.put("/tokens", response_model=AccessTokenResponse)
async def get_refresh_token(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: Annotated[RefreshToken, Depends(valid_refresh_token)],
    user: Annotated[User, Depends(valid_refresh_token_user)],
    db: db_deps,
):
    refresh_token_value = await jwt.create_refresh_token(db, user.id)
    worker.add_task(jwt.expire_refresh_token, db, refresh_token.id)
    response.set_cookie(**get_refresh_token_cookie_settings(refresh_token_value))
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user), refresh_token=refresh_token_value
    )


@auth_router.get("/me", response_model=UserDto)
async def get_current_user(
    db: db_deps, jwt_data: Annotated[JWTData, Depends(jwt.parse_jwt_user_data)]
):
    user = await service.get_user_by_username(db, jwt_data.username)
    return user


@auth_router.delete("/tokens")
async def logout(
    response: Response,
    refresh_token: Annotated[RefreshToken, Depends(valid_refresh_token)],
    db: db_deps,
):
    await jwt.expire_refresh_token(db, refresh_token.id)
    response.delete_cookie(
        **utils.get_refresh_token_cookie_settings(
            refresh_token.refresh_token, expired=True
        )
    )
