from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.config import auth_config
from app.auth.exceptions import AuthRequired, InvalidToken
from app.auth.schemas import JWTData
from app.users.models import User

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
