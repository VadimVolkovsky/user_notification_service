from http import HTTPStatus

from fastapi import APIRouter, Depends
from faststream.rabbit.fastapi import RabbitRouter

from schemas.api_schemas import Notification
from core.config import settings

router = APIRouter()


rabbit_router = RabbitRouter(
    f"amqp://{settings.rabbit_user}:{settings.rabbit_password}@{settings.rabbit_host}:{settings.rabbit_port}/")

@router.post(
    '/add_notification',
    status_code=HTTPStatus.OK,
)
async def add_notification(
        notification: Notification,
):
    """Эндпоинт для добавления нового уведомления в очередь"""
    await rabbit_router.broker.publish(notification, "event")
