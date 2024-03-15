from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.auth import get_hashed_password, get_current_active_user, get_admin
from src.dependencies.dependencies import user_service
from src.model.users import User
from src.schemas.encounters import EncounterSchemaAdd
from src.schemas.monsters import MonsterSchemaAdd
from src.schemas.players import PlayerSchemaAdd
from src.schemas.users import UserSchemaAdd, UserSchemaUpdate, UserSchema
from src.servises.users import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users(
        user_serv: Annotated[UserService, Depends(user_service)],
        admin: Annotated[User, Depends(get_admin)],
        limit: int = 100,
        offset: int = 100
):
    users = await user_serv.get_all_users(limit, offset)
    return {"users": users}


@router.get("/{pk}")
async def get_user(
        pk: int,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user = await user_serv.get_user({"id": pk})
    return {"user": user}


@router.get("/me", response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    return current_user


@router.delete("/")
async def delete_user(
        filters: dict,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user_to_delete = await user_serv.delete_user(filters)
    return {"User deleted": user_to_delete}


@router.put("/")
async def update_user(
        filters: dict,
        user: UserSchemaUpdate,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user_id = await user_serv.update_user(user, filters)
    return {"User info changed": user_id}


@router.post("/")
async def create_user(
        user: UserSchemaAdd,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    created_user = user.model_copy()
    created_user.password = get_hashed_password(user.password)
    user_id = await user_serv.create_user(created_user)
    return {"user": user_id}


@router.get("/me/monsters")
async def get_all_user_monsters(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user_monsters = await user_serv.get_user_monsters(current_user)
    return {f"{current_user.username} players": user_monsters}


@router.get("/me/players")
async def get_all_user_players(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user_players = await user_serv.get_user_players(current_user)
    return {f"{current_user.username} players": user_players}


@router.get("/me/encounters")
async def get_all_user_encounters(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user_players = await user_serv.get_user_encounters(current_user)
    return {f"{current_user.username} encounters": user_players}


@router.post("/me/encounter")
async def create_user_encounter(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)],
        encounter: EncounterSchemaAdd
):
    new_encounter = await user_serv.create_enc_for_user(current_user, encounter)
    return {"Encounter create": new_encounter}


@router.post('/me/monster')
async def create_user_monster(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)],
        monster: MonsterSchemaAdd
):
    new_monster = await user_serv.create_monster_for_user(current_user, monster)
    return {"Monster created": new_monster}


@router.post('/me/player')
async def create_user_monster(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)],
        player: PlayerSchemaAdd
):
    new_player = await user_serv.create_player_for_user(current_user, player)
    return {"Player created": new_player}


@router.put("/me/add_player_to_enc")
async def add_player_to_encounter(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)],
        encounter_id: int,
        player_id: int,
):
    result = await user_serv.add_user_player_to_enc(current_user, encounter_id, player_id)
    return {f"Player {result[0]} has been added to {result[1]}"}


@router.put("/me/add_monster_to_enc")
async def add_monster_to_encounter(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)],
        encounter_id: int,
        monster_id: int,
):
    result = await user_serv.add_user_monster_to_enc(current_user, encounter_id, monster_id)
    return {f"Monster {result[0]} has been added to {result[1]}"}


@router.get('me/encounter/{encounter_id}')
async def get_current_encounter(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)],
        encounter_id: int,
):
    result = await user_serv.show_current_encounter(current_user, encounter_id)
    return {f"{result[0]}": result[1]}
