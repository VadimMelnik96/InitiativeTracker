from sqlalchemy import select

from src.lib.repository import SQLAlchemyRepository
# from src.models import User, Monster, Player, Encounter
from src.model.users import User
from src.model.players import Player
from src.model.monsters import Monster
from src.model.encounters import Encounter
from src.schemas.monsters import MonsterSchema
from src.schemas.players import PlayerSchema
from src.schemas.users import UserSchema


class UserRepository(SQLAlchemyRepository):
    model = User


    async def get_all_users(self):
        result = await self.get_all()
        return [UserSchema.model_validate(row, from_attributes=True) for row in result]


    async def get_user_monsters(self, username: str):
        async with self.session as session:
            stmt = select(Monster).where(self.model.username == username)
            result = await session.execute(stmt)
            return [MonsterSchema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_user_players(self, username: str):
        async with self.session as session:
            stmt = select(Player).where(self.model.username == username)
            result = await session.execute(stmt)
            return [PlayerSchema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_user_encounters(self, username: str):
        async with self.session as session:
            stmt = select(Encounter).where(
                self.model.username == username
            ).order_by(Encounter.id)
            result = await session.execute(stmt)
            return [EncounterSchema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_user_by_username(self, username: str):
        async with self.session as session:
            stmt = select(self.model).where(self.model.username == username)
            user = await session.execute(stmt)
            return user.scalar_one()
