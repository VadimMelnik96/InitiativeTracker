from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_async_session
from src.repositories.encounters import EncounterRepository
from src.servises.encounters import EncounterService
from src.servises.users import UserService
from src.servises.monsters import MonsterService
from src.servises.players import PlayerService
from src.repositories.users import UserRepository
from src.repositories.monsters import MonsterRepository
from src.repositories.players import PlayerRepository


def user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserService(UserRepository(session))


def monster_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return MonsterService(MonsterRepository(session))


def player_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return PlayerService(PlayerRepository(session))


def encounter_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return EncounterService(EncounterRepository(session))
