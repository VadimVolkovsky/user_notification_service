import datetime
import json
from functools import lru_cache

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from crud.event import event_crud
from models.entity import Event
from schemas.api_schemas import EventCreate


class EventService:
    async def add_event(self, event_create: EventCreate, session: AsyncSession):
        """Метод для добавления нового события в БД"""
        evento_dto = jsonable_encoder(event_create)
        date = evento_dto['date']
        evento_dto['date'] = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        event = Event(**evento_dto)
        await event_crud.create_event(event, session)

@lru_cache
def get_event_service() -> EventService:
    return EventService()
