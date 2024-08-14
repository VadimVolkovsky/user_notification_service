from http import HTTPStatus

from fastapi import APIRouter, Depends

from services.notification_service import NotificationService, get_notification_service
from src.schemas.api_schemas import Notification

router = APIRouter()


@router.post(
    '/add_notification',
    status_code=HTTPStatus.OK,
)
async def add_notification(
        notification: Notification,
        notification_service: NotificationService = Depends(get_notification_service),
):
    """Эндпоинт для добавления нового уведомления в очередь"""
    return await notification_service.send_notification_to_queue(notification)
