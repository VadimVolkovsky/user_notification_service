from http import HTTPStatus

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from faststream.rabbit.fastapi import RabbitRouter

from core.config import settings
from schemas.api_schemas import Notification

router = APIRouter()

rabbit_router = RabbitRouter(
    f"amqp://{settings.rabbit_user}:{settings.rabbit_password}@{settings.rabbit_host}:{settings.rabbit_port}/")

access_security = JwtAccessBearer(secret_key=settings.secret_key, auto_error=True)


@router.post("/auth", tags=["auth"])
def auth(user_id: str):
    """Авторизация в сервисе нотификаций"""
    subject = {"user_id": user_id, "role": "admin"}
    return {"access_token": access_security.create_access_token(subject=subject)}


@router.post(
    '/add_notification',
    status_code=HTTPStatus.OK,
    tags=['notifications']
)
async def add_notification(
        notification: Notification,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    """Эндпоинт для добавления нового уведомления в очередь"""
    await rabbit_router.broker.publish(notification, "event")
    return {"status": "Уведомление принято"}
