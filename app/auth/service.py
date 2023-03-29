from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import RegisterDto
from app.auth.utils import PasswordManager
from app.users.models import User


async def register(
    db: AsyncSession,
    data: RegisterDto,
):
    password_manager = PasswordManager()
    existing_user = await db.scalar(select(User).where(User.username == data.username))
    if existing_user:
        raise HTTPException(
            detail="username already exists", status_code=status.HTTP_409_CONFLICT
        )
    new_user = User(**data.dict(exclude={"password"}))
    new_user.password_hash = password_manager.hash(data.password)
    db.add(new_user)
    await db.commit()
    return new_user
