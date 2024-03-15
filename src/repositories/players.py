from src.lib.repository import SQLAlchemyRepository
from src.model.players import Player
from src.schemas.players import PlayerSchema


class PlayerRepository(SQLAlchemyRepository):
    model = Player
    response_dto = PlayerSchema

