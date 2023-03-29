from app.auth.constants import ErrorText
from app.exceptions import Conflict, NotAuthenticated


class UsernameAlreadyExists(Conflict):
    DETAIL = ErrorText.USERNAME_ALREADY_EXISTS


class CredentialsInvalid(NotAuthenticated):
    DETAIL = ErrorText.CREDENTIALS_INVALID


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorText.INVALID_TOKEN


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorText.AUTHENTICATION_REQUIRED
