import random
import string

from app.auth.config import auth_config
from app.config import settings

ALPHA_NUM = string.ascii_letters + string.digits


def generate_random_alpha_num(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def get_refresh_token_cookie_settings(refresh_token: str, expired=False):
    base_cookie = {
        "key": auth_config.REFRESH_TOKEN_KEY,
        "httponly": True,
        "samesite": "none",
        "secure": auth_config.SECURE_COOKIES,
        "domain": settings.SITE_DOMAIN,
    }
    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": auth_config.REFRESH_TOKEN_EXP,
    }
