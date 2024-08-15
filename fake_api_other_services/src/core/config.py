from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    project_name: str = "fake_services"
    fake_app_port: int = 8002

    class Config:
        env_file = BASE_DIR/'.env'
        extra = 'ignore'


settings = Settings()
