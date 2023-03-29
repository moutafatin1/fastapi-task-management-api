from datetime import datetime, timedelta
from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import utils
from app.auth.config import auth_config
from app.auth.exceptions import AuthRequired, InvalidToken
from app.auth.models import RefreshToken, User
from app.auth.schemas import JWTData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def create_access_token(
    user: User, expires_delta=timedelta(minutes=auth_config.JWT_EXP)
):
    payload = {"sub": user.username, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(payload, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


async def parse_jwt_user_data_optional(token: Annotated[str, Depends(oauth2_scheme)]):
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        raise InvalidToken()
    return JWTData(**payload)


async def parse_jwt_user_data(
    token: Annotated[JWTData | None, Depends(parse_jwt_user_data_optional)]
):
    if not token:
        raise AuthRequired()
    return token


async def create_refresh_token(
    db: AsyncSession, user_id: int, refresh_token: str | None = None
):
    if not refresh_token:
        refresh_token = utils.generate_random_alpha_num(64)

    db.add(
        RefreshToken(
            id=uuid4(),
            refresh_token=refresh_token,
            expires_at=datetime.utcnow()
            + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
            user_id=user_id,
        )
    )
    await db.commit()
    return refresh_token


async def get_refresh_token(db: AsyncSession, refresh_token: str):
    return await db.scalar(
        select(RefreshToken).where(RefreshToken.refresh_token == refresh_token)
    )
