from fastapi import APIRouter

from app.database import db_deps
from app.tasks import service
from app.tasks.schemas import TaskCreateDto, TaskDto, TaskUpdateDto

tasks_router = APIRouter(tags=["Tasks"], prefix="/tasks")


@tasks_router.get("/", response_model=list[TaskDto])
async def get_tasks(db: db_deps):
    return await service.get_tasks(db)


@tasks_router.get("/{id}")
async def get_task_by_id(id: int, db: db_deps):
    return await service.get_task_by_id(db, id)


@tasks_router.post("/", response_model=TaskDto)
async def create_task(db: db_deps, data: TaskCreateDto):
    return await service.create_task(db, data)


@tasks_router.put("/{id}")
async def update_task(id: int, db: db_deps, data: TaskUpdateDto):
    return await service.update_task(db, id, data)
