from src.lib.repository import SQLAlchemyRepository
from src.models import Monster


class MonsterRepository(SQLAlchemyRepository):
    model = Monster
