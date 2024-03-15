from src.model.users import User

from src.schemas.users import UserSchemaAdd, UserSchemaUpdate
from src.lib.repository import Repository


class UserService:

    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_user(self, user: UserSchemaAdd):
        new_user = await self.repo.create(user)
        return new_user

    async def get_all_users(self, limit: int = 100, offset: int = 0):
        result = await self.repo.get_list(limit, offset)
        return result

    async def get_user(self, filters: dict):
        result = await self.repo.get_one(**filters)
        return result

    async def get_user_monsters(self, user: User):
        result = await self.repo.get_user_monsters(user)
        return result

    async def update_user(self, new_user: UserSchemaUpdate, filters: dict):
        result = await self.repo.update(new_user, **filters)
        return result

    async def delete_user(self, filters: dict):
        result = await self.repo.delete(**filters)
        return result

    async def get_user_players(self, user):
        result = await self.repo.get_user_players(user)
        return result

    async def get_user_encounters(self, user):
        result = await self.repo.get_user_encounters(user)
        return result

    async def create_enc_for_user(self, user, encounter):
        result = await self.repo.create_new_user_encounter(user, encounter)
        return result

    async def create_monster_for_user(self, user, monster):
        result = await self.repo.create_new_user_monster(user, monster)
        return result

    async def create_player_for_user(self, user, player):
        result = await self.repo.create_new_user_player(user, player)
        return result

    async def add_user_player_to_enc(self, user, encounter_id: int, player_id: int):
        result = await self.repo.add_player_to_user_enc(user, encounter_id, player_id)
        return result

    async def add_user_monster_to_enc(self, user, encounter_id: int, monster_id: int):
        result = await self.repo.add_monster_to_user_enc(user, encounter_id, monster_id)
        return result

    async def show_current_encounter(self, user, encounter_id: int):
        result = await self.repo.get_current_user_enc(user, encounter_id)
        return result

    async def delete_user_enc(self, user, encounter_id: int):
        result = await self.repo.delete_user_enc(user, encounter_id)
        return result
