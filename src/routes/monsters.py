from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies.dependencies import monster_service
from src.schemas.monsters import MonsterSchemaAdd, MonsterSchemaUpdate
from src.servises.monsters import MonsterService

router = APIRouter(
    prefix="/monsters",
    tags=["monsters"]
)

@router.delete("/{id}")
async def delete_monster_by_id(id: int,
                               monster_serv: Annotated[MonsterService, Depends(monster_service)]):
    monster_to_delete = await monster_serv.delete_monster(id)
    return {"monster deleted": monster_to_delete}

@router.get('/')
async def get_all_monsters(monster_serv: Annotated[MonsterService, Depends(monster_service)]):
    monsters = await monster_serv.get_all_monsters()
    return {'monsters': monsters}

@router.get("/{monster_id}")
async def get_monster_by_id(monster_id: int,
                            monster_serv: Annotated[MonsterService, Depends(monster_service)]):
    monster = await monster_serv.get_monster_by_id(monster_id)
    return {"monster": monster}

@router.post("/")
async def create_monster(monster: MonsterSchemaAdd,
                         monster_serv: Annotated[MonsterService, Depends(monster_service)]):
    monster = await monster_serv.create_monster(monster)
    return {"monster_id": monster}

@router.patch("/{monster_id}")
async def update_monster(monster_id: int,
                         monster: MonsterSchemaUpdate,
                         monster_serv: Annotated[MonsterService, Depends(monster_service)]):
    update_monster_id = monster_serv.update_monster(monster_id, monster)
    return {"Monster info changed": update_monster_id}
