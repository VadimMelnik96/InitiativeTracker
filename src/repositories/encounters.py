from sqlalchemy import insert
from sqlalchemy.orm import selectinload
from src.lib.repository import SQLAlchemyRepository
from src.model.encounters import Encounter
from src.model.monsters import Monster
from src.model.players import Player


class EncounterRepository(SQLAlchemyRepository):
    model = Encounter

    async def add_monsters_to_encounter(self, encounter_id: int, monster_id: int):
        async with self.session as session:
            encounter = await session.get(Encounter, encounter_id)
            monster = await session.get(Monster, monster_id)
            encounter.monsters_in_encounter.append(monster)
            await session.commit()
            full_encounter = await session.get(
                Encounter,
                encounter_id,
                options=(selectinload(Encounter.monsters_in_encounter))
            )
            return full_encounter

    async def add_player_to_encounter(self, encounter_id: int, player_id: int):
        async with self.session as session:
            encounter = await session.get(Encounter, encounter_id)
            player = await session.get(Player, player_id)
            encounter.players_in_encounter.append(player)
            await session.commit()
            full_encounter = await session.get(
                Encounter,
                encounter_id,
                options=(selectinload(Encounter.players_in_encounter))
            )
            return full_encounter

    async def add_new_monster_to_encounter(self, encounter_id: int, monster: dict):
        async with self.session as session:
            inserted_monster = insert(Monster).values(**monster).returning(Monster.id)
            result = await session.execute(inserted_monster)
            monster_id = result.scalar_one()
            await session.commit()
            res = await self.add_monsters_to_encounter(encounter_id, monster_id)
            return res

    async def add_new_player_to_encounter(self, encounter_id: int, player: dict):
        async with self.session as session:
            inserted_player = insert(Player).values(**player).returning(Player.id)
            result = await session.execute(inserted_player)
            player_id = result.scalar_one()
            await session.commit()
            res = await self.add_player_to_encounter(encounter_id, player_id)
            return res
