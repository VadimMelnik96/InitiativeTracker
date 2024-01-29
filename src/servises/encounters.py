from src.lib.repository import Repository
from src.schemas.encounters import EncounterSchemaAdd, EncounterSchemaUpdate, EncounterSchema


class EncounterService:

    def __init__(self, repo: Repository):
        self.repo = repo()

    async def create_encounter(self, encounter: EncounterSchemaAdd):
        encounter_dict = encounter.model_dump()
        new_encounter = await self.repo.create(encounter_dict)
        return new_encounter

    async def get_all_encounters(self):
        result = await self.repo.get_all()
        return [EncounterSchema.model_validate(row, from_attributes=True) for row in result]

    async def get_encounters_by_id(self, id: int):
        encounter = await self.repo.get_one(id)
        return encounter

    async def update_encounter_by_id(self, encounter_id: int,
                                     encounter_to_update: EncounterSchemaUpdate):
        new_encounter_data = encounter_to_update.model_dump()
        updated_encounter = await self.repo.update(encounter_id, new_encounter_data)
        return updated_encounter

    async def delete_encounter(self, encounter_id: int):
        result = await self.repo.delete(encounter_id)
        return result

