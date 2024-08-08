from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.api_schemas import Event


class EventService:
    async def add_event(self, event: Event, session: AsyncSession) -> Event:
        """Метод для добавления нового события в БД"""
        ### TODO добавить логику добавления в БД
        return event

@lru_cache
def get_event_service() -> EventService:
    return EventService()
