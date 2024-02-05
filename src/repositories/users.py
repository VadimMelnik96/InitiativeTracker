from sqlalchemy import select

from src.database import async_session
from src.lib.repository import SQLAlchemyRepository
from src.models import User, Monster, Player, Encounter


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_monsters(self, username: str):
        async with async_session() as session:
            stmt = select(Monster).where(self.model.username == username)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_user_players(self, username: str):
        async with async_session() as session:
            stmt = select(Player).where(self.model.username == username)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_user_encounters(self, username: str):
        async with async_session() as session:
            stmt = select(Encounter).where(self.model.username == username).order_by(Encounter.id)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_user_by_username(self, username: str):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.username == username)
            user = await session.execute(stmt)
            return user.scalar_one()
