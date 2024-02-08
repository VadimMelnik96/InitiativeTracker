import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserSchemaAdd(BaseModel):
    username: str
    password: str
    email: str
    active: bool


class UserSchemaUpdate(BaseModel):
    username: str
    password: str
    active: bool


class UserSchemaName(BaseModel):
    username: str
