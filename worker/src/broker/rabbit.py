from faststream.rabbit import RabbitBroker
from core.config import settings

broker = RabbitBroker(
    f"amqp://{settings.rabbit_user}:{settings.rabbit_password}@{settings.rabbit_host}:{settings.rabbit_port}/")


