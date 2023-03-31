from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import jwt, service, utils
from app.auth.dependencies import (
    CurrentUserDep,
    valid_refresh_token,
    valid_refresh_token_user,
)
from app.auth.models import RefreshToken, User
from app.auth.schemas import (
    AccessTokenResponse,
    LoginDto,
    RegisterDto,
    UserDto,
)
from app.auth.utils import get_refresh_token_cookie_settings
from app.database import DbDep

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserDto)
async def register(data: RegisterDto, db: DbDep):
    return await service.register(db, data)


@auth_router.post("/login", response_model=AccessTokenResponse)
async def login(
    db: DbDep,
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
    db: DbDep,
):
    refresh_token_value = await jwt.create_refresh_token(db, user.id)
    worker.add_task(jwt.expire_refresh_token, db, refresh_token.id)
    response.set_cookie(**get_refresh_token_cookie_settings(refresh_token_value))
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user), refresh_token=refresh_token_value
    )


@auth_router.get("/me", response_model=UserDto)
async def get_current_user(user: CurrentUserDep):
    return user


@auth_router.delete("/logout")
async def logout(
    response: Response,
    refresh_token: Annotated[RefreshToken, Depends(valid_refresh_token)],
    db: DbDep,
):
    await jwt.expire_refresh_token(db, refresh_token.id)
    response.delete_cookie(
        **utils.get_refresh_token_cookie_settings(
            refresh_token.refresh_token, expired=True
        )
    )
