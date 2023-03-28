from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks.models import Task


async def get_tasks(db: AsyncSession):
    return (await db.scalars(select(Task))).all()


async def get_task_by_id(db: AsyncSession, id: int):
    task = await db.scalar(select(Task).where(Task.id == id))
    if not task:
        raise HTTPException(
            detail=f"Task with the id {id} does not exists",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return task
