from abc import ABC, abstractmethod

from sqlalchemy import select, insert

from src.database import async_session


class Repository(ABC):

    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_one(self):
        pass




class SQLAlchemyRepository(Repository):

    model = None

    async def create(self, data: dict):
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all(self):
        async with async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_one(self, id: int):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id==id)
            res = await session.execute(stmt)
            return res.scalar_one()