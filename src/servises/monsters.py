from src.schemas.monsters import MonsterSchemaAdd, MonsterSchemaUpdate, MonsterSchema
from src.lib.repository import Repository

class MonsterService:

    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_monster(self, monster: MonsterSchemaAdd):
        new_monster = await self.repo.create(monster)
        return new_monster

    async def get_all_monsters(self):
        result = await self.repo.get_all_monsters()
        return result

    async def get_monster_by_id(self, id: int):
        result = await self.repo.get_one(id)
        return result

    async def update_monster(self, id: int, update_monster: MonsterSchemaUpdate):
        updated_monster = await self.repo.update(id, update_monster)
        return updated_monster

    async def delete_monster(self, monster_id: int):
        monster_to_delete = await self.repo.delete(monster_id)
        return monster_to_delete

