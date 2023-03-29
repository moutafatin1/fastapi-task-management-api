from pydantic import BaseModel


class TaskBaseDto(BaseModel):
    body: str
    completed: bool

    class Config:
        orm_mode = True


class TaskDto(TaskBaseDto):
    id: int
    user_id:int

class TaskCreateDto(BaseModel):
    body: str
    completed: bool | None = None


class TaskUpdateDto(BaseModel):
    body: str | None = None
    completed: bool | None = None
