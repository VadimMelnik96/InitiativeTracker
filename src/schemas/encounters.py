import datetime
from pydantic import BaseModel, ConfigDict


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class EncounterSchema(CustomBaseModel):
    id: int
    encounter_name: str
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class EncounterSchemaAdd(BaseModel):
    encounter_name: str
    user_id: int

class EncounterSchemaAddForUser(BaseModel):
    encounter_name: str

class EncounterSchemaUpdate(BaseModel):
    encounter_name: str
