import datetime
import time

from pydantic import BaseModel


class EventCreate(BaseModel):
    """Схема добавления нового события"""
    type: str
    date: datetime.datetime
    urgent: bool
    payload: dict


class NotificationToSend(EventCreate):
    """Схема готового к отправке уведомления"""
    pass  # TODO дописать доп поля при необходимости
