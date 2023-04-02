from typing import Annotated

from fastapi import APIRouter, Depends

from app.tasks.dependencies import check_task_ownership
from app.tasks.schemas import TaskCreateDto, TaskDto, TaskUpdateDto
from app.tasks.service import TaskService

tasks_router = APIRouter(tags=["Tasks"], prefix="/tasks")

TaskServiceDep = Annotated[TaskService, Depends()]


@tasks_router.get("/", response_model=list[TaskDto])
async def get_tasks(
    task_service: TaskServiceDep,
):
    return await task_service.get_tasks()


@tasks_router.get("/{id}")
async def get_task_by_id(id: int, task_service: TaskServiceDep):
    return await task_service.get_task_by_id(id)


@tasks_router.post("/", response_model=TaskDto)
async def create_task(data: TaskCreateDto, task_service: TaskServiceDep):
    return await task_service.create_task(data)


@tasks_router.put("/{id}", dependencies=[Depends(check_task_ownership)])
async def update_task(
    id: int,
    data: TaskUpdateDto,
    task_service: TaskServiceDep,
):
    return await task_service.update_task(data, id)


@tasks_router.delete("/{id}", dependencies=[Depends(check_task_ownership)])
async def delete_task(id: int, task_service: TaskServiceDep):
    return await task_service.delete_task(id)
