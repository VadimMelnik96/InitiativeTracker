from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.auth import get_admin
from src.dependencies.dependencies import encounter_service
from src.model.users import User
from src.schemas.encounters import EncounterSchemaAdd, EncounterSchemaUpdate
from src.schemas.monsters import MonsterSchemaAdd
from src.schemas.players import PlayerSchemaAdd
from src.servises.encounters import EncounterService

router = APIRouter(prefix="/encounters", tags=["encounters"])


@router.delete("/{id}")
async def delete_encounter_by_id(
        filters: dict,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    encounter_to_delete = await encounter_serv.delete_encounter(filters)
    return {"encounter deleted": encounter_to_delete}


@router.get('/')
async def get_all_encounters(
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)],
        limit: int = 100,
        offset: int = 0
):
    encounters = await encounter_serv.get_all_encounters(limit, offset)
    return {'encounters': encounters}


@router.get("/{encounter_id}")
async def get_encounter(
        filters: dict,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)]
):
    encounter = await encounter_serv.get_encounter(filters)
    return {"encounter": encounter}


@router.post("/")
async def create_encounter(
        encounter: EncounterSchemaAdd,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    encounter = await encounter_serv.create_encounter(encounter)
    return {"encounter_id": encounter}


@router.patch("/{encounter_id}")
async def update_encounter(
        filters: dict,
        encounter: EncounterSchemaUpdate,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    update_encounter_id = encounter_serv.update_encounter_by_id(encounter, filters)
    return {"Encounter info changed": update_encounter_id}


@router.post("/add_monster")
async def add_monster_to_encounter(
        encounter_id: int,
        monster_id: int,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    result = await encounter_serv.add_monster(encounter_id, monster_id)
    return {"Monster added": result}


@router.post("/add_player")
async def add_player_to_encounter(
        encounter_id: int,
        player_id: int,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    result = await encounter_serv.add_player(encounter_id, player_id)
    return {"Player added": result}


@router.post("/add_new_monster")
async def add_new_monster_to_encounter(
        encounter_id: int,
        monster: MonsterSchemaAdd,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    result = await encounter_serv.add_new_monster(encounter_id, monster)
    return {"New Monster added": result}


@router.post("/add_new_player")
async def add_new_player_to_encounter(
        encounter_id: int,
        player: PlayerSchemaAdd,
        encounter_serv: Annotated[EncounterService, Depends(encounter_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    result = await encounter_serv.add_new_player(encounter_id, player)
    return {"New Monster added": result}
