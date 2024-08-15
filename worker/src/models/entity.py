import datetime
import uuid

from sqlalchemy import String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.postgres import Base


class UserSettings(Base):
    """Настройки пользователя"""
    __tablename__ = 'user_settings'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, unique=True, nullable=False)
    allowed_email: Mapped[bool] = mapped_column(Boolean, default=True)
    allowed_push: Mapped[bool] = mapped_column(Boolean, default=True)
    time_zone: Mapped[str] = mapped_column(String(6), nullable=False)