from datetime import datetime
from typing import Annotated

from fastapi import Cookie, Depends

from app.auth import jwt, service
from app.auth.exceptions import AuthRequired, RefreshTokenInvalid
from app.auth.models import RefreshToken, User
from app.auth.schemas import JWTData
from app.database import db_deps


async def valid_refresh_token(
    db: db_deps, refresh_token: str | None = Cookie(alias="refreshToken", default=None)
):
    if not refresh_token:
        raise RefreshTokenInvalid()
    db_refresh_token = await jwt.get_refresh_token(db, refresh_token)
    if not db_refresh_token:
        raise RefreshTokenInvalid()
    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenInvalid()
    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: Annotated[RefreshToken, Depends(valid_refresh_token)], db: db_deps
):
    user = await service.get_user_by_id(db, refresh_token.user_id)
    if not user:
        raise RefreshTokenInvalid()
    return user


async def current_user(
    token: Annotated[JWTData, Depends(jwt.parse_jwt_user_data)], db: db_deps
):
    user = await service.get_user_by_username(db, token.username)
    if not user:
        raise AuthRequired()
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def _is_valid_refresh_token(db_refresh_token: RefreshToken) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at
