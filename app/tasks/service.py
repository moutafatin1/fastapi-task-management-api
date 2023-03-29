from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks.models import Task
from app.tasks.schemas import TaskCreateDto, TaskUpdateDto


async def get_tasks(db: AsyncSession, user_id: int):
    return (await db.scalars(select(Task).where(Task.user_id == user_id))).all()


async def get_task_by_id(db: AsyncSession, id: int):
    task = await db.scalar(select(Task).where(Task.id == id))
    if not task:
        raise HTTPException(
            detail=f"Task with the id {id} does not exists",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return task


async def create_task(db: AsyncSession, data: TaskCreateDto, user_id: int):
    new_task = Task(**data.dict(exclude_none=True), user_id=user_id)
    db.add(new_task)
    await db.commit()
    return new_task


async def update_task(db: AsyncSession, id: int, data: TaskUpdateDto):
    task = await get_task_by_id(db, id)
    await db.execute(
        update(Task).where(Task.id == id).values(**data.dict(exclude_none=True))
    )
    await db.commit()
    return task
