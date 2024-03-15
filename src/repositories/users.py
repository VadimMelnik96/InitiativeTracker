from sqlalchemy import select, insert, delete

from src.infrastructure.database import db_helper
from src.infrastructure.session import ISession
from src.lib.repository import SQLAlchemyRepository
from src.model.users import User
from src.model.players import Player
from src.model.monsters import Monster
from src.model.encounters import Encounter
from src.repositories.encounters import EncounterRepository
from src.repositories.monsters import MonsterRepository
from src.repositories.players import PlayerRepository
from src.schemas.encounters import EncounterSchema, EncounterSchemaAdd
from src.schemas.monsters import MonsterSchema, MonsterSchemaAdd, MonsterSchemaShow
from src.schemas.players import PlayerSchema, PlayerSchemaAdd, PlayerSchemaShow
from src.schemas.users import UserSchema


class UserRepository(SQLAlchemyRepository):
    model = User
    response_dto = UserSchema

    async def get_user_monsters(self, user: User):
        stmt = select(Monster).filter_by(**{"user_id": user.id})
        res = await self._execute(stmt)
        return self.to_dto(res.scalars(), MonsterSchemaShow)

    async def get_user_players(self, user: User):
        stmt = select(Player).filter_by(**{"user_id": user.id})
        res = await self._execute(stmt)
        return self.to_dto(res.scalars(), PlayerSchemaShow)


    async def get_user_encounters(self, user: User):
        stmt = select(Encounter).filter_by(**{"user_id":user.id})
        res = await self._execute(stmt)
        return self.to_dto(res.scalars(), EncounterSchema)

    async def create_new_user_encounter(self, user: User, encounter: EncounterSchemaAdd, auto_commit=True):
        create_encounter = encounter.model_copy()
        create_encounter.user_id = user.id
        stmt = insert(Encounter).values(**create_encounter.model_dump()).returning(Encounter)
        result = await self._execute(stmt)
        await self._flush_or_commit(auto_commit)
        return self.to_dto(result.scalar_one(), EncounterSchema)

    async def create_new_user_monster(self, user: User, monster: MonsterSchemaAdd, auto_commit=True):
        create_monster = monster.model_copy()
        create_monster.user_id = user.id
        stmt = insert(Monster).values(**create_monster.model_dump()).returning(Monster)
        result = await self._execute(stmt)
        await self._flush_or_commit(auto_commit)
        return self.to_dto(result.scalar_one(), MonsterSchemaShow)

    # to player_repo
    async def create_new_user_player(self, user: User, player: PlayerSchemaAdd, auto_commit=True):
        create_player = player.model_copy()
        create_player.user_id = user.id
        stmt = insert(Player).values(**create_player.model_dump()).returning(Player)
        result = await self._execute(stmt)
        await self._flush_or_commit(auto_commit)
        return self.to_dto(result.scalar_one(), PlayerSchemaShow)

    async def add_player_to_user_enc(self, user: User, encounter_id: int, player_id: int, auto_commit=True):
        enc_stmt = select(Encounter).filter_by(**{"id": encounter_id, "user_id": user.id})
        encounter = (await self._execute(enc_stmt)).scalar_one()
        player_stmt = select(Player).filter_by(**{"id": player_id, "user_id": user.id})
        player = (await self._execute(player_stmt)).scalar_one()
        encounter.players_in_encounter.append(player)
        await self._flush_or_commit(auto_commit)
        return player.player_nick, encounter.encounter_name

    async def add_monster_to_user_enc(self, user: User, encounter_id: int, monster_id: int, auto_commit=True):
        enc_stmt = select(Encounter).filter_by(**{"id": encounter_id, "user_id": user.id})
        encounter = (await self._execute(enc_stmt)).scalar_one()
        monster_stmt = select(Monster).filter_by(**{"id": monster_id, "user_id": user.id})
        monster = (await self._execute(monster_stmt)).scalar_one()
        encounter.monsters_in_encounter.append(monster)
        await self._flush_or_commit(auto_commit)
        return monster.monster_nick, encounter.encounter_name

    async def get_current_user_enc(self, user: User, encounter_id: int):
        enc_stmt = select(Encounter).filter_by(**{"id": encounter_id, "user_id": user.id})
        encounter = (await self._execute(enc_stmt)).scalar_one()
        players = self.to_dto(encounter.players_in_encounter, PlayerSchemaShow)
        monsters = self.to_dto(encounter.monsters_in_encounter, MonsterSchemaShow)
        creatures = sorted(
            list(players) + list(monsters),
            key=lambda x: x.initiative, reverse=True)
        return [encounter.encounter_name, creatures]

    async def delete_user_enc(self, user: User, encounter_id: int):
        enc_stmt = delete(Encounter).filter_by(**{"id": encounter_id, "user_id": user.id})
        encounter = (await self._execute(enc_stmt)).scalar_one()
        return encounter.encounter_name
