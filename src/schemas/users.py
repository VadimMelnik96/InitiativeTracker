import datetime
from typing import Optional, List

from fastapi import Form
from pydantic import BaseModel

from src.model.monsters import Monster
from src.model.players import Player
from .encounters import CustomBaseModel


class UserSchema(CustomBaseModel):
    id: int
    username: str
    password: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    active: bool
    is_admin: bool = False


class UserAuthSchema(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(
            cls,
            username: str = Form(...),
            password: str = Form(...),

    ):
        return cls(username=username, password=password)


class UserSchemaAdd(BaseModel):
    username: str
    password: str
    email: str
    active: bool

    @classmethod
    def as_form(
            cls,
            username: str = Form(...),
            password: str = Form(...),
            email: str = Form(...),
    ):
        return cls(username=username, password=password, email=email, active=True)


class UserSchemaAddAdmin(UserSchemaAdd):
    is_admin: bool


class UserSchemaUpdate(BaseModel):
    username: str
    password: str
    active: bool


class UserSchemaName(BaseModel):
    username: str
