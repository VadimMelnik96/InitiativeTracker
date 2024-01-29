from src.schemas.monsters import MonsterSchemaAdd, MonsterSchemaUpdate, MonsterSchema
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
        return [MonsterSchema.model_validate(row, from_attributes=True) for row in result]

    async def get_monster_by_id(self, id: int):
        result = await self.repo.get_one(id)
        return result

    async def update_monster(self, id: int, update_monster: MonsterSchemaUpdate):
        monster_dict = update_monster.model_dump()
        updated_monster = await self.repo.update(id, monster_dict)
        return updated_monster

    async def delete_monster(self, monster_id: int):
        monster_to_delete = await self.repo.delete(monster_id)
        return monster_to_delete

