from src.lib.repository import Repository
from src.schemas.encounters import EncounterSchemaAdd, EncounterSchemaUpdate, EncounterSchema
from src.schemas.monsters import MonsterSchemaAdd
from src.schemas.players import PlayerSchemaAdd


class EncounterService:

    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_encounter(self, encounter: EncounterSchemaAdd):
        new_encounter = await self.repo.create(encounter)
        return new_encounter

    async def get_all_encounters(self, limit: int = 100, offset: int = 100):
        result = await self.repo.get_list(limit, offset)
        return result

    async def get_encounter(self, filters: dict):
        encounter = (await self.repo.get_one(**filters)).model_validate(self.repo.model)
        creatures = sorted(
            list(encounter.players_in_encounter) + list(encounter.monsters_in_encounter),
            key=lambda x: x.initiative, reverse=True)
        return [encounter.encounter_name, creatures]

    async def update_encounter_by_id(
            self,
            filters: dict,
            encounter_to_update: EncounterSchemaUpdate
    ):
        updated_encounter = await self.repo.update(encounter_to_update, **filters)
        return updated_encounter

    async def delete_encounter(self, filters: dict):
        result = await self.repo.delete(**filters)
        return result

    async def add_monster(self, encounter_id: int, monster_id: int):
        result = await self.repo.add_monsters_to_encounter(encounter_id, monster_id)
        return result

    async def add_player(self, encounter_id: int, player_id: int):
        result = await self.repo.add_player_to_encounter(encounter_id, player_id)
        return result

    async def add_new_monster(self, encounter_id: int, monster: MonsterSchemaAdd):
        monster_dict = monster.model_dump()
        result = await self.repo.add_new_monster_to_encounter(encounter_id, monster_dict)
        return result

    async def add_new_player(self, encounter_id: int, player: PlayerSchemaAdd):
        player_dict = player.model_dump()
        result = await self.repo.add_new_player_to_encounter(encounter_id, player_dict)
        return result

