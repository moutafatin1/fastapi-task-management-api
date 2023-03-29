from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import UsernameAlreadyExists
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
        raise UsernameAlreadyExists()
    new_user = User(**data.dict(exclude={"password"}))
    new_user.password_hash = password_manager.hash(data.password)
    db.add(new_user)
    await db.commit()
    return new_user
