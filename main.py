from datetime import timedelta
from typing import Annotated

import jwt
import uvicorn
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from fastapi.responses import RedirectResponse, Response

from config import JWT_SECRET_KEY
from src.auth.token_schemas import Token, TokenData
from src.dependencies.dependencies import user_service
from src.model.users import User
from src.routes import monsters, users, players, encounters
from src.auth.auth import auth_router, get_hashed_password, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, get_current_active_user, ALGORITHM
from src.schemas.users import UserSchemaAdd, UserAuthSchema
from src.servises.users import UserService

app = FastAPI(title="Initiative Tracker")

templates = Jinja2Templates(directory='templates')

app.include_router(users.router)
app.include_router(monsters.router)
app.include_router(players.router)
app.include_router(encounters.router)
app.include_router(auth_router)

@app.get("/", response_class=HTMLResponse)
async def main_page(
        request: Request,

):
    return templates.TemplateResponse(
                                      'index.html',
                                      context={"request": request}
                                      )

#@app.post("/form", response_model=SimpleModel)
#async def form_post(no: int = Form(...),nm: str = Form(...)):
    #return SimpleModel(no=no,nm=nm)

@app.get("/registration", response_class=HTMLResponse)
async def registration_form(request: Request):
    return templates.TemplateResponse('registration.html', context={"request": request})


@app.post("/registration")
async def register_user(
        user_serv: Annotated[UserService, Depends(user_service)],
        new_user: UserSchemaAdd = Depends(UserSchemaAdd.as_form),
):
    new_user.password = get_hashed_password(new_user.password)
    user_id = await user_serv.create_user(new_user)
    return {"New user has been added": user_id}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=True)