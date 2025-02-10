from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from data_base.models import User
from data_base.database import async_session

async def get_users_list_from_db():
    async with async_session() as session:  # Контекстный менеджер для сессии
        result = await session.execute(select(User))  # Используем select вместо query
        users = result.scalars().all()  # Получаем все строки как объекты User
    return users
