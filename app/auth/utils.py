from passlib.context import CryptContext


class PasswordManager:
    def __init__(self) -> None:
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def verify_and_update(
        self, password: str, password_hash: str
    ) -> tuple[bool, str | None]:
        return self.verify_and_update(password, password_hash)
