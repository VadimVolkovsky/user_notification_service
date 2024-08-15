import uuid
import abc
from typing import TypeAlias, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.entity import UserSettings
from schemas.models import UserSettings as UserSettingsSchema


EntityItem: TypeAlias = UserSettings
EntityItemSchema: TypeAlias = UserSettingsSchema


class Storage(abc.ABC):
    @abc.abstractmethod
    async def create(self, entity: Any, session: Any) -> Any:
        pass

    @abc.abstractmethod
    async def get(self, entity_id: Any, session: Any) -> Any:
        pass

    @abc.abstractmethod
    async def get_all_users(self, entity: Any, schema: Any, session: Any) -> Any:
        pass


class PostgresStorage(Storage):
    """Класс для работы с моделью в БД"""
    def __init__(self, model: Type[EntityItem]) -> None:
        self._model = model

    async def create(self, entity: Type[EntityItem], session: AsyncSession) -> Type[EntityItem]:
        """Создание нового события в БД"""
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

    async def get(self, entity_id: uuid.UUID, session: AsyncSession) -> Type[EntityItem]:
        """Создание нового события в БД"""
        entity = await session.get(self._model, entity_id)

        if entity:
            return entity

    async def get_all_users(
            self, entity: Type[EntityItem], schema: Type[EntityItemSchema], session: AsyncSession
    ) -> list[Type[EntityItemSchema],]:
        entities = await session.execute(select(entity))
        if entities:
            return [schema.model_validate(i) for i in entities.scalars()]
