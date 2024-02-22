from sqlalchemy import select, insert, delete
from src.lib.repository import SQLAlchemyRepository
from src.model.users import User
from src.model.players import Player
from src.model.monsters import Monster
from src.model.encounters import Encounter
from src.schemas.encounters import EncounterSchema, EncounterSchemaAdd
from src.schemas.monsters import MonsterSchema, MonsterSchemaAdd, MonsterSchemaShow
from src.schemas.players import PlayerSchema, PlayerSchemaAdd, PlayerSchemaShow
from src.schemas.users import UserSchema


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_all_users(self):
        result = await self.get_all()
        return [UserSchema.model_validate(row, from_attributes=True) for row in result]

    async def get_user_monsters(self, user: User):
        async with self.session as session:
            stmt = select(Monster).where(self.model.username == user.username)
            result = await session.execute(stmt)
            return [MonsterSchema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_user_players(self, user: User):
        async with self.session as session:
            stmt = select(Player).where(self.model.username == user.username)
            result = await session.execute(stmt)
            return [PlayerSchema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_user_encounters(self, user: User):
        async with self.session as session:
            stmt = select(Encounter).where(
                self.model.username == user.username
            ).order_by(Encounter.id)
            result = await session.execute(stmt)
            return [EncounterSchema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_user_by_username(self, username: str):
        async with self.session as session:
            stmt = select(self.model).where(self.model.username == username)
            user = await session.execute(stmt)
            return user.scalar_one()

    # to encounter_repo
    async def create_new_user_encounter(self, user: User, encounter: EncounterSchemaAdd):
        async with self.session as session:
            create_encounter = encounter.model_copy()
            create_encounter.user_id = user.id
            stmt = insert(Encounter).values(**create_encounter.model_dump()).returning(Encounter.id)
            new_enc = await session.execute(stmt)
            await session.commit()
            return new_enc.scalar_one()

    # to monster_repo
    async def create_new_user_monster(self, user: User, monster: MonsterSchemaAdd):
        async with self.session as session:
            create_monster = monster.model_copy()
            create_monster.user_id = user.id
            stmt = insert(Monster).values(**create_monster.model_dump()).returning(Monster.id)
            new_monster = await session.execute(stmt)
            await session.commit()
            return new_monster.scalar_one()

    # to player_repo
    async def create_new_user_player(self, user: User, player: PlayerSchemaAdd):
        async with self.session as session:
            create_player = player.model_copy()
            create_player.user_id = user.id
            stmt = insert(Player).values(**create_player.model_dump()).returning(Player.id)
            new_player = await session.execute(stmt)
            await session.commit()
            return new_player.scalar_one()
    # to enc_repo???
    async def add_player_to_user_enc(self, user: User, encounter_id: int, player_id: int):
        async with self.session as session:
            encounter_stmt = select(Encounter).where(
                Encounter.id == encounter_id,
                Encounter.user_id == user.id
            )
            result1 = await session.execute(encounter_stmt)
            encounter = result1.scalar_one()
            player_stmt = select(Player).where(Player.id == player_id, Player.user_id == user.id)
            result2 = await session.execute(player_stmt)
            player = result2.scalar_one()
            encounter.players_in_encounter.append(player)
            await session.commit()
            return player.player_nick, encounter.encounter_name

    #to monster_repo??
    async def add_monster_to_user_enc(self, user: User, encounter_id: int, monster_id: int):
        async with self.session as session:
            encounter_stmt = select(Encounter).where(
                Encounter.id == encounter_id,
                Encounter.user_id == user.id
            )
            result1 = await session.execute(encounter_stmt)
            encounter = result1.scalar_one()
            monster_stmt = select(Monster).where(Monster.id == monster_id, Monster.user_id == user.id)
            result2 = await session.execute(monster_stmt)
            monster = result2.scalar_one()
            encounter.monsters_in_encounter.append(monster)
            await session.commit()
            return monster.monster_nick, encounter.encounter_name

    async def get_current_user_enc(self, user: User, encounter_id: int):
        async with self.session as session:
            encounter_stmt = select(Encounter).where(
                Encounter.id == encounter_id,
                Encounter.user_id == user.id
            )
            result1 = await session.execute(encounter_stmt)
            encounter = result1.scalar_one()
            players = [PlayerSchemaShow.model_validate(row, from_attributes=True) for row in
                       encounter.players_in_encounter]
            monsters = [MonsterSchemaShow.model_validate(row, from_attributes=True) for row in
                        encounter.monsters_in_encounter]
            creatures = sorted(
                list(players) + list(monsters),
                key=lambda x: x.initiative, reverse=True)
            return [encounter.encounter_name, creatures]

    async def delete_user_enc(self, user: User, encounter_id: int):
        async with self.session as session:
            stmt = delete(Encounter).where(
                Encounter.id == encounter_id,
                Encounter.user_id == user.id
            )
            result = await session.execute(stmt)
            deleted_enc = result.scalar_one()
            return deleted_enc.encounter_name
