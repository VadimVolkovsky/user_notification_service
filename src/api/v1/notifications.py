from http import HTTPStatus

from fastapi import APIRouter

from src.schemas.api_schemas import Event

router = APIRouter()


@router.post(
    '/add_notification',
    status_code=HTTPStatus.OK,
)
async def add_notification(
        event: Event,
        # notification_service: NotificationService = Depends(get_notification_service),  # TODO
        # session: AsyncSession = Depends(get_session)  # TODO Postgresql
):
    print(f'Получено событие {event.type}')

