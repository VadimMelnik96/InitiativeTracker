from src.schemas.monsters import MonsterSchemaAdd, MonsterSchemaUpdate, MonsterSchema
from src.lib.repository import Repository

class MonsterService:

    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_monster(self, monster: MonsterSchemaAdd):
        new_monster = await self.repo.create(monster)
        return new_monster

    async def get_all_monsters(self, limit: int = 100, offset: int = 0):
        result = await self.repo.get_list(limit, offset)
        return result

    async def get_monster_by_id(self, filters: dict):
        result = await self.repo.get_one(**filters)
        return result

    async def update_monster(self, update_monster: MonsterSchemaUpdate, filters: dict):
        updated_monster = await self.repo.update(update_monster, **filters)
        return updated_monster

    async def delete_monster(self, filters: dict):
        monster_to_delete = await self.repo.delete(**filters)
        return monster_to_delete

