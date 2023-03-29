from pydantic import BaseModel, Field


class UserDto(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class AuthBaseDto(BaseModel):
    username: str
    password: str


class LoginDto(AuthBaseDto):
    pass


class RegisterDto(AuthBaseDto):
    pass


class JWTData(BaseModel):
    username: str = Field(alias="sub")


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
