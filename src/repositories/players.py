#from src.models import Player
from src.lib.repository import SQLAlchemyRepository
from src.model.players import Player
from src.schemas.players import PlayerSchema


class PlayerRepository(SQLAlchemyRepository):
    model = Player

    async def get_all_players(self):
        result = await self.get_all()
        return [PlayerSchema.model_validate(row, from_attributes=True) for row in result]
