from src.model.base import Base, created_at, updated_at
from typing import List
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    email: Mapped[str]
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    monsters: Mapped[List["Monster"]] = relationship(back_populates="user")
    players: Mapped[List["Player"]] = relationship(back_populates="user")
    encounters: Mapped[List["Encounter"]] = relationship(back_populates="user")
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
