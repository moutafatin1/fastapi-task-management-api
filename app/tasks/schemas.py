from pydantic import BaseModel


class TaskDto(BaseModel):
    id: int
    body: str
    completed: bool

    class Config:
        orm_mode = True
