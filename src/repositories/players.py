#from src.models import Player
from src.lib.repository import SQLAlchemyRepository
from src.model.players import Player


class PlayerRepository(SQLAlchemyRepository):
    model = Player
