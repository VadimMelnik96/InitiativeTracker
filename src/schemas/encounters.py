from pydantic import BaseModel

class EncounterSchema(BaseModel):
    id: int
    encounter_name: str
    user_id: int

class EncounterSchemaAdd(BaseModel):
    encounter_name: str
    user_id: int

class EncounterSchemaUpdate(BaseModel):
    encounter_name: str
