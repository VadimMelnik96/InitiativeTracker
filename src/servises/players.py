from src.schemas.players import PlayerSchemaAdd, PlayerSchemaUpdate, PlayerSchema
from src.lib.repository import Repository


class PlayerService:

    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_player(self, player: PlayerSchemaAdd):
        new_player = await self.repo.create(player)
        return new_player

    async def get_all_players(self):
        players = await self.repo.get_all()
        return [PlayerSchema.model_validate(row, from_attributes=True) for row in players]

    async def get_player_by_id(self, player_id: int):
        player = await self.repo.get_one(player_id)
        return player

    async def update_player(self, player_id: int,
                            update_player: PlayerSchemaUpdate):
        updated_player = await self.repo.update(player_id, update_player)
        return updated_player

    async def delete_player(self, player_id: int):
        player_to_delete = await self.repo.delete(player_id)
        return player_to_delete