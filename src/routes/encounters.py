from typing import Annotated

from fastapi import APIRouter, Depends
from src.dependencies.dependencies import encounter_service
from src.schemas.encounters import EncounterSchemaAdd, EncounterSchemaUpdate
from src.schemas.monsters import MonsterSchemaAdd
from src.schemas.players import PlayerSchemaAdd
from src.servises.encounters import EncounterService

router = APIRouter(prefix="/encounters", tags=["encounters"])


@router.delete("/{id}")
async def delete_encounter_by_id(
        id: int,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    encounter_to_delete = await encounter_serv.delete_encounter(id)
    return {"encounter deleted": encounter_to_delete}


@router.get('/')
async def get_all_encounters(encounter_serv: Annotated[EncounterService, Depends(encounter_service)]):
    encounters = await encounter_serv.get_all_encounters()
    return {'encounters': encounters}


@router.get("/{encounter_id}")
async def get_encounter_by_id(
        encounter_id: int,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    encounter = await encounter_serv.get_encounters_by_id(encounter_id)
    return {"encounter": encounter}


@router.post("/")
async def create_encounter(
        encounter: EncounterSchemaAdd,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    encounter = await encounter_serv.create_encounter(encounter)
    return {"encounter_id": encounter}


@router.patch("/{encounter_id}")
async def update_encounter(
        encounter_id: int,
        encounter: EncounterSchemaUpdate,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    update_encounter_id = encounter_serv.update_encounter_by_id(encounter_id, encounter)
    return {"Encounter info changed": update_encounter_id}

@router.post("/add_monster")
async def add_monster_to_encounter(
        encounter_id: int,
        monster_id: int,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    result = await encounter_serv.add_monster(encounter_id, monster_id)
    return {"Monster added": result}


@router.post("/add_player")
async def add_monster_to_encounter(
        encounter_id: int,
        player_id: int,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    result = await encounter_serv.add_player(encounter_id, player_id)
    return {"Player added": result}



@router.post("/add_new_monster")
async def add_new_monster_to_encounter(
        encounter_id: int,
        monster: MonsterSchemaAdd,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]

):
    result = await encounter_serv.add_new_monster(encounter_id, monster)
    return {"New Monster added": result}


@router.post("/add_new_player")
async def add_new_player_to_encounter(
        encounter_id: int,
        player: PlayerSchemaAdd,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    result = await encounter_serv.add_new_player(encounter_id, player)
    return {"New Monster added": result}

