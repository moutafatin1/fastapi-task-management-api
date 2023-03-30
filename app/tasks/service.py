from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, update

from app.auth.dependencies import CurrentUserDep
from app.database import DbDep
from app.tasks.models import Task
from app.tasks.schemas import TaskCreateDto, TaskUpdateDto


class TaskService:
    def __init__(self, db: DbDep, user: CurrentUserDep) -> None:
        self.db = db
        self.user = user

    async def get_tasks(self):
        return (
            await self.db.scalars(select(Task).where(Task.user_id == self.user.id))
        ).all()

    async def get_task_by_id(self, id: int):
        task = await self.db.scalar(
            select(Task).where(Task.id == id).where(Task.user_id == self.user.id)
        )
        if not task:
            raise HTTPException(
                detail=f"Task with the id {id} does not exists",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return task

    async def create_task(self, data: TaskCreateDto):
        new_task = Task(**data.dict(exclude_none=True), user_id=self.user.id)
        self.db.add(new_task)
        await self.db.commit()
        return new_task

    async def update_task(self, data: TaskUpdateDto, id: int):
        task = await self.get_task_by_id(id)
        await self.db.execute(
            update(Task).where(Task.id == id).values(**data.dict(exclude_none=True))
        )
        await self.db.commit()
        return task


