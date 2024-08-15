from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    project_name: str = "notification_service"
    secret_key: str = ""
    app_port: int = 8000

    postgres_host: str = ""
    postgres_port: int = 5432
    postgres_db: str = ""
    postgres_user: str = ""
    postgres_password: str = ""
    echo: bool = False  # вывод операций с БД в логи

    rabbit_host: str = ""
    rabbit_port: str = 5672
    rabbit_user: str = "guest"
    rabbit_password: str = "guest"

    user_data_url: str = 'http://127.0.0.1:8002/api/v1/user_info'
    film_data_url: str = 'http://127.0.0.1:8002/api/v1/film_info'

    night_hour_min: str = '01:00'
    night_hour_max: str = '05:00'

    ### PROD config ###
    smtp_server: str = ""
    smtp_port: str = ""

    sender_login: str = ""
    sender_email: str = ""
    sender_password: str = ""
    sender_name: str = ""


    ### DEBUG config (для локальной отладки) ###
    smtp_server_debug: str = "localhost"
    smtp_port_debug: int = 1025

    debug: bool = True


    class Config:
        env_file = BASE_DIR/'.env'
        extra = 'ignore'


settings = Settings()
