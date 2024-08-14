import datetime
import time

from pydantic import BaseModel


class EventCreate(BaseModel):
    """Схема добавления нового события"""
    type: str
    date: datetime.datetime
    urgent: bool
    payload: dict


class Notification(BaseModel):
    """Схема отправки уведомления в API"""
    title = str
    type = str
    channel = str
    recipients = dict
    created_at = datetime.datetime
    context = dict
