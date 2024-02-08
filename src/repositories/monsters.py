from src.lib.repository import SQLAlchemyRepository
# from src.models import Monster
from src.model.monsters import Monster


class MonsterRepository(SQLAlchemyRepository):
    model = Monster
