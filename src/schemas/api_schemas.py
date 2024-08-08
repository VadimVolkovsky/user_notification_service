import datetime
import time

from pydantic import BaseModel


class Event(BaseModel):
    """Схема добавления нового события"""
    type: str
    datetime: datetime.datetime
    urgent: bool
    payload: dict
