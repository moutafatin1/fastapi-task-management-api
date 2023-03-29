from app.auth.constants import ErrorText
from app.exceptions import Conflict


class UsernameAlreadyExists(Conflict):
    DETAIL = ErrorText.USERNAME_ALREADY_EXISTS
