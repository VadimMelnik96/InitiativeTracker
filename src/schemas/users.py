from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: str


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
