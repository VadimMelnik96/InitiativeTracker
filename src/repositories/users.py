from src.lib.repository import SQLAlchemyRepository
from src.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
