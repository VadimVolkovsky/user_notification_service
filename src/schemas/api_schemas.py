import datetime
import uuid

from pydantic import BaseModel


class Recipient(BaseModel):
    id: uuid.UUID
    email: str | None
    name: str | None


class Context(BaseModel):
    films_list: list | None  # список новых фильмов
    episode_number = str | None  # номер новой серии
    message: str | None  # сообщение для пользователя


class Notification(BaseModel):
    """Схема отправки уведомления в API"""
    title: str
    type: str
    channel: str
    recipients: list[Recipient]
    created_at: datetime.datetime
    context: Context


class NotificationToSend(BaseModel):
    """Схема отправки уведомления в сендер"""
    title: str
    type: str
    recipients: list[Recipient]
    context: Context
