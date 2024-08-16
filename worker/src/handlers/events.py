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
from notification_sender.sender import get_sender, NotificationSender

broker = RabbitBroker(
    f"amqp://{settings.rabbit_user}:{settings.rabbit_password}@{settings.rabbit_host}:{settings.rabbit_port}/")


exchange_delayed = RabbitExchange("exchange", type=ExchangeType.X_DELAYED_MESSAGE, durable=True)
queue_delayed_email = RabbitQueue("delayed_email")
queue_urgent_email = RabbitQueue("urgent_email")


@broker.subscriber(queue=queue_urgent_email)
@broker.subscriber(queue=queue_delayed_email, exchange=exchange_delayed)
async def handle_email_notification(
        message: NotificationToSend,
        sender: NotificationSender = Depends(get_sender)
):
    sender.send_notification_by_email(message)


@broker.subscriber("event")
async def handle_event(
        message: Notification,
        session: AsyncSession = Depends(get_session),
        user_service: UserSettingsService = Depends(get_user_setting_service),
):
    delay = Delay(user_service)
    tz = {}
    if message.type == "new_user":
        print(message)
        user_id = message.recipients[0].id
        await user_service.add_user(user_id, session)   # TODO удалить при наличии реальной бд
        user = await user_service.get_user(user_id, session)

        if user.allowed_email and message.channel == 'email':
            user_data = await user_service.get_user_info(user)
            tz.update({user.time_zone: [user_data]})
            await delay.notificate(tz, message, queue_delayed_email, queue_urgent_email)

    elif message.type == "new_episode":
        for recipient in message.recipients:
            user = await user_service.get_user(recipient.id, session)
            if not user:
                user = await user_service.add_user(recipient.id, session)   # TODO удалить при наличии реальной бд

            if user.allowed_email and message.channel == 'email':
                user_data = await user_service.get_user_info(user)
                if user.time_zone not in tz.keys():
                    tz.update({user.time_zone: [user_data]})
                else:
                    tz[user.time_zone].append(user_data)
        if tz:
            await delay.notificate(tz, message, queue_delayed_email, queue_urgent_email)


class Delay:
    def __init__(self, user_service: UserSettingsService):
        self._user_service = user_service

    async def notificate(self, tz, message, queue_delayed, queue_urgent):
        for time_zone, users in tz.items():
            output = NotificationToSend(
                recipients=users, title=message.title, type=message.type, context=message.context
            )
            if self._user_service.is_active(time_zone):
                await broker.publish(output, queue=queue_urgent)
            else:
                delay = self._user_service.get_delay(time_zone)
                await broker.publish(output, queue=queue_delayed, exchange=exchange_delayed, headers={"x-delay": delay})
