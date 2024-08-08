from logging import config as logging_config
from pathlib import Path

from pydantic_settings import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


BASE_DIR = PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    project_name: str = "notification_service"
    secret_key: str = ""
    app_port: int = 8000

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = Settings()
