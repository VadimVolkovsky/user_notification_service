from notification_sender.sender import NotificationSender
from schemas.models import (
    Notification,
    NotificationToSend
)
from services.user import UserSettingsService, get_user_setting_service
from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from faststream.rabbit import RabbitExchange, ExchangeType, RabbitQueue
from db.postgres import get_session

from faststream.rabbit import RabbitBroker
from core.config import settings

broker = RabbitBroker(
    f"amqp://{settings.rabbit_user}:{settings.rabbit_password}@{settings.rabbit_host}:{settings.rabbit_port}/")


exchange_delayed = RabbitExchange("exchange", type=ExchangeType.X_DELAYED_MESSAGE, durable=True)
queue_delayed_email = RabbitQueue("delayed_email")
queue_urgent_email = RabbitQueue("urgent_email")


@broker.subscriber(queue=queue_urgent_email)
@broker.subscriber(queue=queue_delayed_email, exchange=exchange_delayed)
async def handle_email_notification(
        message: NotificationToSend
):
    sender = NotificationSender()
    sender.send_notification_by_email(message)


@broker.subscriber("event")
async def handle_event(
        message: Notification,
        session: AsyncSession = Depends(get_session),
        user_service: UserSettingsService = Depends(get_user_setting_service),
):
    delay = Delay(user_service)
    if message.type == "new_user":
        user_id = message.recipients[0].id
        await user_service.add_user(user_id, session)   # TODO удалить при наличии реальной бд
        user = await user_service.get_user(user_id, session)

        if user.allowed_email and message.channel == 'email':
            await delay.notificate(user, message, queue_delayed_email, queue_urgent_email)

    elif message.type == "new_series":
        for recipient in message.recipients:
            user = await user_service.get_user(recipient.id, session)
            if not user:
                user = await user_service.add_user(recipient.id, session)   # TODO удалить при наличии реальной бд
            if user.allowed_email and message.channel == 'email':
                await delay.notificate(user, message, queue_delayed_email, queue_urgent_email)


class Delay:
    def __init__(self, user_service: UserSettingsService):
        self._user_service = user_service

    async def notificate(self, user, message, queue_delayed, queue_urgent):
        user_data = await self._user_service.get_user_info(user)
        output = NotificationToSend(
            recipient=user_data, title=message.title, type=message.type, context=message.context
        )
        if user_data and self._user_service.is_active(user.time_zone):
            await broker.publish(output, queue=queue_urgent)
        else:
            delay = self._user_service.get_delay(user.time_zone)
            await broker.publish(output, queue=queue_delayed, exchange=exchange_delayed, headers={"x-delay": delay})
