from src.lib.repository import SQLAlchemyRepository
from src.model.monsters import Monster
from src.schemas.monsters import MonsterSchema


class MonsterRepository(SQLAlchemyRepository):
    model = Monster

    async def get_all_monsters(self):
        result = await self.get_all()
        return [MonsterSchema.model_validate(row, from_attributes=True) for row in result]
