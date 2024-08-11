import datetime
import uuid

from sqlalchemy import String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.db.postgres import Base

# Новые модели необходимо импортировать в файле src/db/base.py чтобы алембик их увидел при миграциях


class Event(Base):
    """Схема добавления нового события"""
    __tablename__ = 'events'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    date: Mapped[datetime.datetime]
    urgent: Mapped[bool] = mapped_column(Boolean)
    payload: Mapped[JSON] = mapped_column(JSON)
