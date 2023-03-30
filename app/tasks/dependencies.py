from sqlalchemy import select

from app.auth.dependencies import CurrentUserDep
from app.database import DbDep
from app.exceptions import Conflict
from app.tasks.exceptions import TaskNotFound
from app.tasks.models import Task


async def check_task_ownership(id: int, user: CurrentUserDep, db: DbDep) -> None:
    task = await db.scalar(select(Task).where(Task.id == id))
    if not task:
        raise TaskNotFound(id)
    if task.user_id != user.id:
        raise Conflict()


