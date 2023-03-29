from pydantic import BaseModel


class UserDto(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
