from pydantic import BaseModel


class TaskBaseDto(BaseModel):
    body: str
    completed: bool

    class Config:
        orm_mode = True


class TaskDto(TaskBaseDto):
    id: int


class TaskCreateDto(TaskBaseDto):
    completed: bool | None = None
