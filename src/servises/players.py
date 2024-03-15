from src.schemas.players import PlayerSchemaAdd, PlayerSchemaUpdate, PlayerSchema
from src.lib.repository import Repository


class PlayerService:

    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_player(self, player: PlayerSchemaAdd):
        new_player = await self.repo.create(player)
        return new_player

    async def get_all_players(self, limit: int = 100, offset: int = 0):
        players = await self.repo.get_list(limit, offset)
        return players

    async def get_player(self, filters: dict):
        player = await self.repo.get_one(**filters)
        return player

    async def update_player(self,
                            update_player: PlayerSchemaUpdate, filters: dict):
        updated_player = await self.repo.update(update_player, **filters)
        return updated_player

    async def delete_player(self, filters: dict):
        player_to_delete = await self.repo.delete(**filters)
        return player_to_delete
