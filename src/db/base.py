"""
Импорты класса Base и всех моделей для Alembic.
При создании новой модели, необходимо добавить ее сюда, чтобы алембик смог ее увидеть
"""
from src.db.postgres import Base
from src.models.entity import Event
