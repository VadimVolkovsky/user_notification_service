import datetime
import time

from pydantic import BaseModel


class EventCreate(BaseModel):
    """Схема добавления нового события"""
    type: str
    date: datetime.datetime
    urgent: bool
    payload: dict


class NotificationToSend(BaseModel):
    """Схема готового к отправке уведомления"""
    type: str
    subject: str
    message: str
    payload: list[dict]



