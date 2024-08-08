from sqlalchemy.ext.asyncio import AsyncSession

from models.entity import Event


class CRUDEvent:
    """Класс для работы с моделью Event в БД"""

    async def create_event(self, event: Event, session: AsyncSession) -> Event:
        """Создание нового события в БД"""
        session.add(event)
        await session.commit()
        await session.refresh(event)
        return event


event_crud = CRUDEvent()
