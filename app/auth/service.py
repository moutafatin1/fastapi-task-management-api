from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import CredentialsInvalid, UsernameAlreadyExists
from app.auth.models import User
from app.auth.schemas import LoginDto, RegisterDto
from app.auth.security import hash_password, verify_and_update_password


async def get_user_by_username(db: AsyncSession, username: str):
    return await db.scalar(select(User).where(User.username == username))


async def get_user_by_id(db: AsyncSession, id: int):
    return await db.scalar(select(User).where(User.id == id))


async def register(
    db: AsyncSession,
    data: RegisterDto,
):
    existing_user = await db.scalar(select(User).where(User.username == data.username))
    if existing_user:
        raise UsernameAlreadyExists()
    new_user = User(**data.dict(exclude={"password"}))
    new_user.password_hash = hash_password(data.password)
    db.add(new_user)
    await db.commit()
    return new_user


async def login(db: AsyncSession, data: LoginDto):
    user = await get_user_by_username(db, data.username)
    if not user:
        raise CredentialsInvalid()

    verified, new_password_hash = verify_and_update_password(
        data.password, user.password_hash
    )
    if not verified:
        raise CredentialsInvalid()

    if new_password_hash is not None:
        user.password_hash = new_password_hash
        await db.commit()
    return user
