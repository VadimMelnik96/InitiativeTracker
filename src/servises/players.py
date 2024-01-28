from src.schemas.players import PlayerSchemaAdd, PlayerSchemaUpdate
from src.lib.repository import Repository


class PlayerService:

    def __init__(self, repo: Repository):
        self.repo = repo()

    async def create_player(self, player: PlayerSchemaAdd):
        player_dict = player.model_dump()
        new_player = await self.repo.create(player_dict)
        return new_player

    async def get_all_players(self):
        players = await self.repo.get_all()
        return players

    async def get_player_by_id(self, player_id: int):
        player = await self.repo.get_one(player_id)
        return player

    async def update_player(self, player_id: int,
                            update_player: PlayerSchemaUpdate):
        updated_player = await self.repo.update(player_id, update_player)
        return updated_player