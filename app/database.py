from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
