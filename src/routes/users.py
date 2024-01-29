from typing import Annotated

from fastapi import APIRouter, Depends
from src.dependencies.dependencies import user_service
from src.schemas.users import UserSchemaAdd, UserSchemaUpdate
from src.servises.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/")
async def get_users(user_serv: Annotated[UserService, Depends(user_service)]):
    users = await user_serv.get_all_users()
    return {"users": users}

@router.get("/{id}")
async def get_user_by_id(id: int,
                         user_serv: Annotated[UserService, Depends(user_service)]):
    user = await user_serv.get_user_by_id(id)
    return {"user": user}

@router.delete("/{id}")
async def delete_user_by_id(id: int,
                            user_serv: Annotated[UserService, Depends(user_service)]):
    user_to_delete = await user_serv.delete_user(id)
    return {"User deleted": user_to_delete}

@router.patch("{id}")
async def update_user(id: int,
                      user: UserSchemaUpdate,
                      user_serv: Annotated[UserService, Depends(user_service)]
                      ):
    user_id = await user_serv.update_user(id, user)
    return {"User info changed": user_id}

@router.post("/")
async def create_user(user: UserSchemaAdd,
                      user_serv: Annotated[UserService, Depends(user_service)]):
    user_id = await user_serv.create_user(user)
    return {"user_id": user_id}
