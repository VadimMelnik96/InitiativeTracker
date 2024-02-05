from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.auth import get_hashed_password, get_current_active_user
from src.dependencies.dependencies import user_service
from src.models import User
from src.schemas.users import UserSchemaAdd, UserSchemaUpdate, UserSchema
from src.servises.users import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users(user_serv: Annotated[UserService, Depends(user_service)]):
    users = await user_serv.get_all_users()
    return {"users": users}


@router.get("/{id}")
async def get_user_by_id(
        id: int,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user = await user_serv.get_user_by_id(id)
    return {"user": user}


@router.get("/user_info/{username}")
async def get_user_by_username(
        username: str,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user = await user_serv.get_user_by_username(username)

    return {"user": user}


@router.get("/me", response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    return current_user


@router.delete("/{id}")
async def delete_user_by_id(
        id: int,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user_to_delete = await user_serv.delete_user(id)
    return {"User deleted": user_to_delete}


@router.patch("/{id}")
async def update_user(
        id: int,
        user: UserSchemaUpdate,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user_id = await user_serv.update_user(id, user)
    return {"User info changed": user_id}


@router.post("/")
async def create_user(
        user: UserSchemaAdd,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    created_user = user.model_copy()
    created_user.password = get_hashed_password(user.password)
    user_id = await user_serv.create_user(created_user)
    return {"user_id": user_id}


@router.get("/me/monsters")
async def get_all_user_monsters(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)]
):
    username = current_user.username
    user_monsters = await user_serv.get_user_monsters(username)
    return {f"{username} monsters": user_monsters}


@router.get("/me/players")
async def get_all_user_players(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)]
):
    username = current_user.username
    user_players = await user_serv.get_user_players(username)
    return {f"{username} players": user_players}


@router.get("/me/encounters")
async def get_all_user_encounters(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_serv: Annotated[UserService, Depends(user_service)]
):
    username = current_user.username
    user_players = await user_serv.get_user_encounters(username)
    return {f"{username} encounters": user_players}
