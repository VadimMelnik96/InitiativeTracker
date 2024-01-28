from typing import Optional, List

from pydantic import BaseModel, ConfigDict
from src.models import Condition

class CustomBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class MonsterSchema(CustomBaseModel):
    id: int
    user_id: int
    initiative: int = 0
    monster_nick: str
    armour_class: int
    hp: int
    conditions: Optional[List[Condition]]
    concentration: bool = False
    note: str


class MonsterSchemaAdd(CustomBaseModel):
    user_id: int
    initiative: int = 0
    monster_nick: str
    armour_class: int
    hp: int
    conditions: Optional[List[Condition]]
    concentration: bool = False
    note: str


class MonsterSchemaUpdate(CustomBaseModel):
    initiative: int = 0
    monster_nick: str
    armour_class: int
    hp: int
    conditions: Optional[List[Condition]]
    concentration: bool = False
    note: str

