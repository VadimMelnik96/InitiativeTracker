from src.schemas.users import UserSchemaAdd
from src.utils.repository import Repository

class UserService:

    def __init__(self, repo:Repository):
        self.repo = repo()

    async def create_user(self, user: UserSchemaAdd):
            user_dict = user.model_dump()
            new_user = await self.repo.create(user_dict)
            return new_user

    async def get_all_users(self):
        result = await self.repo.get_all()
        return result

    async def get_user_by_id(self, id: int):
        result = await self.repo.get_one(id)
        return result