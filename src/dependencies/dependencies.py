from src.servises.users import UserService
from src.servises.monsters import MonsterService
from src.servises.players import PlayerService
from src.repositories.users import UserRepository
from src.repositories.monsters import MonsterRepository
from src.repositories.players import PlayerRepository

def user_service():
    return UserService(UserRepository)

def monster_service():
    return MonsterService(MonsterRepository)

def player_service():
    return PlayerService(PlayerRepository)