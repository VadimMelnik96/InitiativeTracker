from typing import Optional, List

from pydantic import BaseModel, ConfigDict
from src.models import Condition


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class PlayerSchema(CustomBaseModel):
    id: int
    user_id: int
    initiative: int = 0
    player_nick: str
    armour_class: int
    conditions: Optional[List[Condition]]
    concentration: bool = False
    note: str


class PlayerSchemaAdd(CustomBaseModel):
    user_id: int
    initiative: int = 0
    player_nick: str
    armour_class: int
    conditions: Optional[List[Condition]]
    concentration: bool = False
    note: str


class PlayerSchemaUpdate(CustomBaseModel):
    initiative: int = 0
    player_nick: str
    armour_class: int
    conditions: Optional[List[Condition]]
    concentration: bool = False
    note: str
