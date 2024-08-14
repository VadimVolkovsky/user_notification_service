from functools import lru_cache

from starlette.responses import JSONResponse

from schemas.api_schemas import NotificationToSend


class NotificationService:
    async def send_notification_to_queue(self, notification: NotificationToSend):
        """Метод для отправки уведомления в очередь RabbitMQ"""
        # await send_to_rabbitmq(queue_name, notification)  # TODO
        return JSONResponse({"message": "Уведомление успешно отправлено в очередь"})


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()
