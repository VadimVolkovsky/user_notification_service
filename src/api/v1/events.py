from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from services.event_service import EventService, get_event_service
from src.schemas.api_schemas import EventCreate

router = APIRouter()


@router.post(
    '/add_event',
    status_code=HTTPStatus.OK,
)
async def add_event(
        event: EventCreate,
        event_service: EventService = Depends(get_event_service),
        session: AsyncSession = Depends(get_session)
):
    """Эндпоинт для добавления нового события"""
    await event_service.add_event(event, session)
    # print(f'Добавлено событие {event.type}')  ### TODO DEBUG ONLY


