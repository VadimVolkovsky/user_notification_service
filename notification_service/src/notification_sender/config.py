from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Конфиг для сендера"""
    ### PROD config ###
    smtp_server: str
    smtp_port: str

    sender_login: str
    sender_email: str
    sender_password: str
    sender_name: str


    ### DEBUG config (для локальной отладки) ###
    smtp_server_debug: str = "localhost"
    smtp_port_debug: int = 25

    class Config:
        env_file = '../.env'
        extra = 'ignore'


settings = Settings()
