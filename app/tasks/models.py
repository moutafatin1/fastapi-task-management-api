from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, get_db


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


async def seed_db():
    db_gen = get_db()
    db = await anext(db_gen)
    db.add_all(
        [
            Task(body="First task"),
            Task(body="Second task"),
            Task(body="Third task"),
        ]
    )
    await db.commit()
    await db.close()
