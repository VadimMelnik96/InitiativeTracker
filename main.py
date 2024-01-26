from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends

from src.dependencies.dependencies import user_service
from src.schemas.users import UserSchemaAdd
from src.servises.users import UserService

app = FastAPI(title="Initiative Tracker")


@app.get("/users")
async def get_users(user_serv: Annotated[UserService, Depends(user_service)]):
    users = await user_serv.get_all_users()
    return {"users": users}

@app.get("/users/{id}")
async def get_user_by_id(id: int,
                         user_serv: Annotated[UserService, Depends(user_service)]):
    user = await user_serv.get_user_by_id(id)
    return {"user":user}

@app.post("/users")
async def create_user(user: UserSchemaAdd,
                      user_serv: Annotated[UserService, Depends(user_service)]):
    user_id = await user_serv.create_user(user)
    return {"user_id": user_id}


if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=True)