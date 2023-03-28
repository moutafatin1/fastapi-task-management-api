from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, get_db, setup_db

app = FastAPI(title="Task Management API", version="1.0.0")


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


class TestDto(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


@app.on_event("startup")
async def init_db():
    await setup_db()


@app.get("/", response_model=list[TestDto])
async def root(db: Annotated[AsyncSession, Depends(get_db)]):
    lists = await db.scalars(select(Test))
    return lists.all()


@app.get("/seed")
async def seed(db: Annotated[AsyncSession, Depends(get_db)]):
    db.add(Test(title="Second Data"))
    await db.commit()
