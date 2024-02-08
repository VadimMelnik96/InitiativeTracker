import datetime
import enum
from typing import  Annotated
from sqlalchemy.orm import DeclarativeBase, mapped_column


created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.now())]
updated_at = Annotated[datetime.datetime, mapped_column(
    default=datetime.datetime.now(),
    onupdate=datetime.datetime.now
)]


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
