from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.auth import get_admin
from src.dependencies.dependencies import monster_service
from src.model.users import User
from src.schemas.monsters import MonsterSchemaAdd, MonsterSchemaUpdate
from src.servises.monsters import MonsterService

router = APIRouter(prefix="/monsters", tags=["monsters"])


@router.delete("/{id}")
async def delete_monster_by_id(
        filters: dict,
        monster_serv: Annotated[MonsterService, Depends(monster_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    monster_to_delete = await monster_serv.delete_monster(filters)
    return {"monster deleted": monster_to_delete}


@router.get('/')
async def get_all_monsters(
        monster_serv: Annotated[MonsterService, Depends(monster_service)],
        admin: Annotated[User, Depends(get_admin)],
        limit: int = 100,
        offset: int = 0
):
    monsters = await monster_serv.get_all_monsters(limit, offset)
    return {'monsters': monsters}


@router.get("/{monster_id}")
async def get_monster(
        filters: dict,
        monster_serv: Annotated[MonsterService, Depends(monster_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    monster = await monster_serv.get_monster_by_id(filters)
    return {"monster": monster}


@router.post("/")
async def create_monster(
        monster: MonsterSchemaAdd,
        monster_serv: Annotated[MonsterService, Depends(monster_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    monster = await monster_serv.create_monster(monster)
    return {"monster_id": monster}


@router.patch("/{monster_id}")
async def update_monster(
        filters: dict,
        monster: MonsterSchemaUpdate,
        monster_serv: Annotated[MonsterService, Depends(monster_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    update_monster_id = monster_serv.update_monster(monster, filters)
    return {"Monster info changed": update_monster_id}
