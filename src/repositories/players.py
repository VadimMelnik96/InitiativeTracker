from src.models import Player
from src.lib.repository import SQLAlchemyRepository


class PlayerRepository(SQLAlchemyRepository):
    model = Player
