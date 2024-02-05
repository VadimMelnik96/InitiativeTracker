from src.schemas.encounters import EncounterSchema
from src.schemas.monsters import MonsterSchema
from src.schemas.players import PlayerSchema
from src.schemas.users import UserSchemaAdd, UserSchemaUpdate, UserSchema, UserSchemaName
from src.lib.repository import Repository


class UserService:

    def __init__(self, repo: Repository):
        self.repo = repo()

    async def create_user(self, user: UserSchemaAdd):
        user_dict = user.model_dump()
        new_user = await self.repo.create(user_dict)
        return new_user

    async def get_all_users(self):
        result = await self.repo.get_all()
        return [UserSchema.model_validate(row, from_attributes=True) for row in result]

    async def get_user_by_id(self, id: int):
        result = await self.repo.get_one(id)
        return result

    async def get_user_monsters(self, username: str):
        result = await self.repo.get_user_monsters(username)
        return [MonsterSchema.model_validate(row, from_attributes=True) for row in result]

    async def get_user_by_username(self, username: str):
        result = await self.repo.get_user_by_username(username)
        return result

    async def update_user(self, id: int, new_user: UserSchemaUpdate):
        user_dict = new_user.model_dump()
        result = await self.repo.update(id, user_dict)
        return result

    async def delete_user(self, id: int):
        result = await self.repo.delete(id)
        return result

    async def get_user_players(self, username: str):
        result = await self.repo.get_user_players(username)
        return [PlayerSchema.model_validate(row, from_attributes=True) for row in result]

    async def get_user_encounters(self, username: str):
        result = await self.repo.get_user_encounters(username)
        return [EncounterSchema.model_validate(row, from_attributes=True) for row in result]
