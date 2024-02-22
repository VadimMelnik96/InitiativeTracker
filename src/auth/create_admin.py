import asyncio

from sqlalchemy import insert
from src.infrastructure.database import db_helper
from src.model.users import User
from config import ADMIN_PASSWORD, ADMIN_USERNAME, ADMIN_EMAIL
from src.schemas.users import UserSchemaAddAdmin
from auth import get_hashed_password


async def create_admin(admin_data: UserSchemaAddAdmin):
    async with db_helper.get_db_session() as session:
        stmt = insert(User).values(**admin_data.model_dump()).returning(User.id)
        await session.execute(stmt)
        await session.commit()

password = get_hashed_password(ADMIN_PASSWORD)
admin = {"username": ADMIN_USERNAME, "password": password, "email": ADMIN_EMAIL, "active": True, "is_admin": True}
to_base = UserSchemaAddAdmin(**admin)
asyncio.run(create_admin(to_base))
