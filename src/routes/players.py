from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.auth import get_admin
from src.dependencies.dependencies import player_service
from src.model.users import User
from src.schemas.players import PlayerSchemaAdd, PlayerSchemaUpdate
from src.servises.players import PlayerService

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
async def get_all_players(
        player_serv: Annotated[PlayerService, Depends(player_service)],
        admin: Annotated[User, Depends(get_admin)],
        limit: int = 100,
        offset: int = 0
):
    players = await player_serv.get_all_players(limit, offset)
    return {"players": players}


@router.get("/{pk}")
async def get_player(
        pk: int,
        player_serv: Annotated[PlayerService, Depends(player_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    player = await player_serv.get_player({"id": pk})
    return {"player": player}


@router.post("/")
async def create_player(
        player: PlayerSchemaAdd,
        player_serv: Annotated[PlayerService, Depends(player_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    player = await player_serv.create_player(player)
    return {"Player created": player}


@router.patch("/")
async def update_player(
        filters: dict,
        update_player: PlayerSchemaUpdate,
        player_serv: Annotated[PlayerService, Depends(player_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    updated_player = await player_serv.update_player(update_player, filters)
    return {"Player info updated": updated_player}


@router.delete("/{id}")
async def delete_player_by_id(
        filters: dict,
        player_serv: Annotated[PlayerService, Depends(player_service)],
        admin: Annotated[User, Depends(get_admin)]
):
    player_to_delete = await player_serv.delete_player(filters)
    return {"player deleted": player_to_delete}
