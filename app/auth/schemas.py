from pydantic import BaseModel


class AuthBaseDto(BaseModel):
    username: str
    password: str


class LoginDto(AuthBaseDto):
    pass


class RegisterDto(AuthBaseDto):
    pass
