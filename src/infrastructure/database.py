from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import DB_NAME, DB_PASS, DB_PORT, DB_HOST, DB_USER


class Settings:
    DATABASE_URL_async = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?async_fallback=True"

    def get_session_fabric(self):
        engine = create_async_engine(url=self.DATABASE_URL_async, echo=True, pool_size=5, max_overflow=10)
        return async_sessionmaker(engine)



# DATABASE_URL_async = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?async_fallback=True"
# async_engine = create_async_engine(url=DATABASE_URL_async, echo=True, pool_size=5, max_overflow=10)

# async_session = async_sessionmaker(async_engine)

database = Settings()
async_session = database.get_session_fabric()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session