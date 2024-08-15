from pydantic import BaseModel
import uuid
import datetime


class UserSettings(BaseModel):
    """Настройки пользователя"""
    id: uuid.UUID
    allowed_email: bool
    allowed_push: bool
    time_zone: str

    class Config:
        from_attributes = True


class Recipient(BaseModel):
    id: uuid.UUID
    email: str | None = None
    name: str | None = None


class Context(BaseModel):
    films_list: list | None = None  # список новых фильмов
    episode_number: int | None = None  # номер новой серии
    message: str | None = None  # сообщение для пользователя


class Notification(BaseModel):
    """Схема отправки уведомления в API"""
    title: str
    type: str
    channel: str
    recipients: list[Recipient]
    created_at: datetime.datetime
    context: Context


class NotificationToSend(BaseModel):
    """Схема отправки уведомления из воркера в сендер"""
    title: str
    type: str
    recipient: Recipient # recipients: list[Recipient]
    context: Context
