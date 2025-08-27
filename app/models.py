from sqlalchemy import String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import Annotated

pk = Annotated[int, mapped_column(Integer, primary_key=True, index=True)]

class User(Base):
    __tablename__ = "users"

    id: Mapped[pk]
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")
