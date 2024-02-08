from src.model.base import Base, created_at, updated_at, Condition
from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Monster(Base):
    __tablename__ = "monsters"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    initiative: Mapped[int] = mapped_column(default=0)
    monster_nick: Mapped[str] = mapped_column(String(120))
    armour_class: Mapped[int]
    hp: Mapped[int]
    conditions: Mapped[Optional[List[Condition]]] = mapped_column(ARRAY(ENUM(
        Condition,
        name="condition",
        create_type=False)),
        nullable=True
    )
    concentration: Mapped[bool] = mapped_column(default=False)
    note: Mapped[str] = mapped_column(String(300), nullable=True)
    user: Mapped["User"] = relationship(back_populates="monsters")
    monster_encounters: Mapped[List["Encounter"]] = relationship(
        back_populates="monsters_in_encounter",
        secondary="encountered_monsters",
        lazy="selectin"

    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]