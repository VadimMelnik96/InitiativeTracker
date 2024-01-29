from typing import Annotated

from fastapi import APIRouter, Depends
from src.dependencies.dependencies import encounter_service
from src.schemas.encounters import EncounterSchemaAdd, EncounterSchemaUpdate
from src.servises.encounters import EncounterService

router = APIRouter(
    prefix="/encounters",
    tags=["encounters"]
)


@router.delete("/{id}")
async def delete_encounter_by_id(id: int,
                                 encounter_serv: Annotated[EncounterService, Depends(encounter_service)]):
    encounter_to_delete = await encounter_serv.delete_encounter(id)
    return {"encounter deleted": encounter_to_delete}


@router.get('/')
async def get_all_encounters(encounter_serv: Annotated[EncounterService, Depends(encounter_service)]):
    encounters = await encounter_serv.get_all_encounters()
    return {'encounters': encounters}


@router.get("/{encounter_id}")
async def get_encounter_by_id(encounter_id: int,
                              encounter_serv: Annotated[EncounterService, Depends(encounter_service)]):
    encounter = await encounter_serv.get_encounters_by_id(encounter_id)
    return {"encounter": encounter}


@router.post("/")
async def create_encounter(encounter: EncounterSchemaAdd,
                           encounter_serv: Annotated[EncounterService, Depends(encounter_service)]):
    encounter = await encounter_serv.create_encounter(encounter)
    return {"encounter_id": encounter}


@router.patch("/{encounter_id}")
async def update_monster(encounter_id: int,
                         encounter: EncounterSchemaUpdate,
                         encounter_serv: Annotated[EncounterService, Depends(encounter_service)]):
    update_encounter_id = encounter_serv.update_encounter_by_id(encounter_id, encounter)
    return {"Encounter info changed": update_encounter_id}
