import enum
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Подумать насчет энума для истощений
class Condition(enum.Enum):
    BLINDED = "Blinded"
    CHARMED = "Charmed"
    DEAFENED = "Deafened"
    FRIGHTENED = "Frightened"
    INCAPACITATED = "Incapacitated"
    INVISIBLE = "Invisible"
    PARALYZED = "Paralyzed"
    PETRIFIED = "Petrified"
    POISONED = "Poisoned"
    PRONE = "Prone"
    RESTRAINED = "Restrained"
    STUNNED = "Stunned"
    UNCONSCIOUS = "Unconscious"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    monsters: Mapped[List["Monster"]] = relationship(back_populates="user")
    players: Mapped[List["Player"]] = relationship(back_populates="user")
    encounters: Mapped[List["Encounter"]] = relationship(back_populates="user")


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    initiative: Mapped[int] = mapped_column(default=0)
    player_nick: Mapped[str] = mapped_column(String(120))
    armour_class: Mapped[int]
    conditions: Mapped[List["Condition"]] = mapped_column(ARRAY(String))
    concentration: Mapped[bool] = mapped_column(default=False)
    note: Mapped[str] = mapped_column(String(300), nullable=True)
    user: Mapped["User"] = relationship(back_populates="players")
    player_encounters: Mapped[List["Encounter"]] = relationship(back_populates="players_in_encounter",
                                                                secondary="encountered_players")


class Monster(Base):
    __tablename__ = "monsters"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    initiative: Mapped[int] = mapped_column(default=0)
    monster_nick: Mapped[str] = mapped_column(String(120))
    armour_class: Mapped[int]
    hp: Mapped[int]
    conditions: Mapped[Optional[List["Condition"]]] = mapped_column(ARRAY(String))
    concentration: Mapped[bool] = mapped_column(default=False)
    note: Mapped[str] = mapped_column(String(300), nullable=True)
    user: Mapped["User"] = relationship(back_populates="monsters")
    monster_encounters: Mapped[List["Encounter"]] = relationship(back_populates="monsters_in_encounter",
                                                                 secondary="encountered_monsters")


class Encounter(Base):
    __tablename__ = "encounters"
    id: Mapped[int] = mapped_column(primary_key=True)
    encounter_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="encounters")
    monsters_in_encounter: Mapped[List["Monster"]] = relationship(back_populates="monster_encounters",
                                                                  secondary="encountered_monsters")
    players_in_encounter: Mapped[List["Player"]] = relationship(back_populates="player_encounters",
                                                                secondary="encountered_players")


class EncounteredPlayers(Base):
    __tablename__ = "encountered_players"
    encounter_id: Mapped[int] = mapped_column(ForeignKey("encounters.id", ondelete="CASCADE"), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), primary_key=True)


class EncounteredMonsters(Base):
    __tablename__ = "encountered_monsters"
    encounter_id: Mapped[int] = mapped_column(ForeignKey("encounters.id", ondelete="CASCADE"), primary_key=True)
    monster_id: Mapped[int] = mapped_column(ForeignKey("monsters.id", ondelete="CASCADE"), primary_key=True)
