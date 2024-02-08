from src.model.base import Base, created_at, updated_at
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Encounter(Base):
    __tablename__ = "encounters"
    id: Mapped[int] = mapped_column(primary_key=True)
    encounter_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="encounters")
    monsters_in_encounter: Mapped[List["Monster"]] = relationship(
        back_populates="monster_encounters",
        secondary="encountered_monsters",
        lazy="selectin"
    )
    players_in_encounter: Mapped[List["Player"]] = relationship(
        back_populates="player_encounters",
        secondary="encountered_players",
        lazy="selectin"
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class EncounteredPlayers(Base):
    __tablename__ = "encountered_players"
    encounter_id: Mapped[int] = mapped_column(ForeignKey(
        "encounters.id",
        ondelete="CASCADE"),
        primary_key=True
    )
    player_id: Mapped[int] = mapped_column(ForeignKey(
        "players.id",
        ondelete="CASCADE"),
        primary_key=True
    )


class EncounteredMonsters(Base):
    __tablename__ = "encountered_monsters"
    encounter_id: Mapped[int] = mapped_column(ForeignKey(
        "encounters.id",
        ondelete="CASCADE"),
        primary_key=True
    )
    monster_id: Mapped[int] = mapped_column(ForeignKey(
        "monsters.id",
        ondelete="CASCADE"),
        primary_key=True
    )
