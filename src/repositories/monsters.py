from src.lib.repository import SQLAlchemyRepository
from src.model.monsters import Monster
from src.schemas.monsters import MonsterSchema


class MonsterRepository(SQLAlchemyRepository):
    model = Monster
    response_dto = MonsterSchema
