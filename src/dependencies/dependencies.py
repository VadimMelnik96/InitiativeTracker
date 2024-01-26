from src.servises.users import UserService
from src.repositories.users import UserRepository

def user_service():
    return UserService(UserRepository)