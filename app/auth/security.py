from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return context.hash(password)


def verify_and_update_password(
    password: str, password_hash: str
) -> tuple[bool, str | None]:
    return context.verify_and_update(password, password_hash)
