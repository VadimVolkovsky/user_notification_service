import datetime

from pydantic import BaseModel


class Recipient(BaseModel):
    email: str
    name: str


class Notification(BaseModel):
    """Схема отправки уведомления в API"""
    title: str
    type: str
    channel: str
    recipients: list[Recipient]
    created_at: datetime.datetime
    context: dict
