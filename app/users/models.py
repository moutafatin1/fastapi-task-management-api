from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.tasks.models import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    tasks: Mapped[list[Task]] = relationship(back_populates="user")
