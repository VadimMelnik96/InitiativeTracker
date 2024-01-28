from src.schemas.monsters import MonsterSchemaAdd, MonsterSchemaUpdate
from src.lib.repository import Repository

class MonsterService:

    def __init__(self, repo: Repository):
        self.repo = repo()

    async def create_monster(self, monster: MonsterSchemaAdd):
        monster_dict = monster.model_dump()
        new_monster = await self.repo.create(monster_dict)
        return new_monster

    async def get_all_monsters(self):
        result = await self.repo.get_all()
        return result

    async def get_monster_by_id(self, id: int):
        result = await self.repo.get_one(id)
        return result

    async def update_monster(self, update_monster: MonsterSchemaUpdate):
        monster_dict = update_monster.model_dump()
        updated_monster = await self.repo.update(monster_dict)
        return updated_monster

