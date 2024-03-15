from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from src.lib.repository import SQLAlchemyRepository
from src.model.encounters import Encounter
from src.model.monsters import Monster
from src.model.players import Player
from src.repositories.monsters import MonsterRepository
from src.repositories.players import PlayerRepository
from src.schemas.encounters import EncounterSchema
from src.schemas.monsters import MonsterSchemaAdd
from src.schemas.players import PlayerSchemaAdd


class EncounterRepository(SQLAlchemyRepository):
    model = Encounter
    response_dto = EncounterSchema


    async def add_monsters_to_encounter(self, encounter_id: int, monster_id: int, auto_commit = True):
        enc_stmt = select(Encounter).filter_by(**{"id": encounter_id})
        encounter = (await self._execute(enc_stmt)).scalar_one()
        monster_stmt = select(Monster).filter_by(**{"id": monster_id})
        monster = (await self._execute(monster_stmt)).scalar_one()
        encounter.monsters_in_encounter.append(monster)
        await self._flush_or_commit(auto_commit)
        full_encounter = await self.session.get(
                Encounter,
                encounter_id,
                options=(selectinload(Encounter.monsters_in_encounter))
            )
        return full_encounter

    async def add_player_to_encounter(self, encounter_id: int, player_id: int, auto_commit = True):
        enc_stmt = select(Encounter).filter_by(**{"id": encounter_id})
        encounter = (await self._execute(enc_stmt)).scalar_one()
        player_stmt = select(Player).filter_by(**{"id": player_id})
        player = (await self._execute(player_stmt)).scalar_one()
        encounter.players_in_encounter.append(player)
        await self._flush_or_commit(auto_commit)
        full_encounter = await self.session.get(
            Encounter,
            encounter_id,
            options=(selectinload(Encounter.players_in_encounter))
        )
        return full_encounter

    async def add_new_monster_to_encounter(self, encounter_id: int, monster: MonsterSchemaAdd):
        stmt = insert(Monster).values(**monster.model_dump()).returning(Monster)
        new_monster = (await self._execute(stmt)).scalar_one()
        res = await self.add_monsters_to_encounter(encounter_id, new_monster.id)
        return res

    async def add_new_player_to_encounter(self, encounter_id: int, player: PlayerSchemaAdd):
        stmt = insert(Player).values(**player.model_dump()).returning(Player)
        new_player = (await self._execute(stmt)).scalar_one()
        res = await self.add_monsters_to_encounter(encounter_id, new_player.id)
        return res
