from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete

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

    @abstractmethod
    async def update(self):
        pass

    @abstractmethod
    async def delete(self):
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
            return res.scalars().all()

    async def get_one(self, id: int):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def update(self, id: int, data: dict):
        async with async_session() as session:
            stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, id: int):
        async with async_session() as session:
            stmt = delete(self.model).filter_by(id=id)
            res = await session.execute(stmt)
            await session.commit()
            return res
