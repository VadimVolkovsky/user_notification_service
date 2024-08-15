import datetime
import uuid
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from storage.postgres import PostgresStorage, Storage
from models.entity import UserSettings
from schemas.models import UserSettings as UserSettingsSchema
from core.config import settings


from services.request import RequestService


class UserSettingsService:
    _client: PostgresStorage
    NIGHT_HOUR_MIN = settings.night_hour_min
    NIGHT_HOUR_MAX = settings.night_hour_max

    def __init__(
        self,
    ) -> None:
        self._client: Storage = PostgresStorage(UserSettings)
        self._request: RequestService = RequestService()

    async def add_user(self, user_id: uuid.UUID, session: AsyncSession) -> UserSettingsSchema:
        """Добавление нового пользователя в БД"""
        user_settings = UserSettings(id=user_id, time_zone='+05:00')
        user_settings_db = await self._client.create(user_settings, session)
        return UserSettingsSchema.model_validate(user_settings_db)

    async def get_user(self, entity_id: uuid.UUID, session: AsyncSession) -> UserSettingsSchema:
        """Получение пользователя из БД"""
        user_db = await self._client.get(entity_id, session)
        if user_db:
            user = UserSettingsSchema.model_validate(user_db)
            return user

    async def get_all_users(self, session: AsyncSession):
        """Получение всех пользователей из БД"""
        result = await self._client.get_all_users(UserSettings, UserSettingsSchema, session)
        return result

    @staticmethod
    def get_user_tz_offset(time_zone: str) -> datetime.timedelta:
        """Получение таймзоны пользователя"""
        hours, minutes = time_zone.split(":")
        offset = datetime.timedelta(hours=int(hours), minutes=int(minutes))
        return offset

    def is_active(self, time_zone: str) -> bool:
        """Проверка на возможность отправить уведомление в не ночное время"""
        user_time = self.get_user_time(time_zone)
        night_hour_min = datetime.datetime.strptime(self.NIGHT_HOUR_MIN, "%H:%M").time()
        night_hour_max = datetime.datetime.strptime(self.NIGHT_HOUR_MAX, "%H:%M").time()
        if not night_hour_min <= user_time.time() < night_hour_max:
            return True
        return False

    def get_user_time(self, time_zone: str) -> datetime.datetime:
        """Получение локального времени пользователя"""
        offset = self.get_user_tz_offset(time_zone)
        now = datetime.datetime.utcnow()
        user_time = now + offset
        return user_time

    def get_delay(self, time_zone: str) -> int:
        """Получение задержки на которую необходимо отложить отправку"""
        night_hour_max = datetime.datetime.strptime(self.NIGHT_HOUR_MAX, "%H:%M").time()
        user_time = self.get_user_time(time_zone)
        time_delta = datetime.timedelta(minutes=10)
        while True:
            user_time = user_time + time_delta
            time_delta = time_delta + datetime.timedelta(minutes=10)
            if user_time.time() > night_hour_max:
                break
        delay = int(time_delta.total_seconds() * 1000)
        return delay

    async def get_user_info(self, user):
        """Получение данных пользователя"""
        user_data = await self._request.user_info(user)
        return user_data


@lru_cache
def get_user_setting_service() -> UserSettingsService:
    return UserSettingsService()
