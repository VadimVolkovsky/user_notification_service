import os
import logging
import smtplib
from email.message import EmailMessage

from jinja2 import FileSystemLoader, Environment

from core.config import settings
from notification_sender.smtp import connect_to_smtp, connect_to_smtp_debug
from schemas.models import NotificationToSend

logger = logging.getLogger("__name__")


class NotificationSender:
    """Класс для подготовки и отправки уведомления пользователю"""

    def __init__(self):
        self._loader = FileSystemLoader(searchpath=f'{os.path.dirname(__file__)}/templates')
        self.env = Environment(loader=self._loader)

    def _create_email_notification(self, notification: NotificationToSend) -> EmailMessage:
        """Подготовка уведомления для отправки по email"""
        email_data = {
            "greeting": f"Привет {notification.recipient.name} !",
            "message": notification.context.message,
            "sender_name": settings.sender_name,
        }

        message = EmailMessage()
        message['From'] = settings.sender_email
        message['To'] = notification.recipient.email
        message['Subject'] = notification.title

        template = self.env.get_template(f'{notification.type}.html')
        output = template.render(**email_data)
        message.add_alternative(output, subtype='html')
        return message

    def send_notification_by_email(self, notification: NotificationToSend):
        """Отправка уведомления пользователю по email"""
        msg = self._create_email_notification(notification)
        if not msg:
            logger.exception('Нет сообщений для отправки')
            return

        if settings.debug:
            smtp_server = connect_to_smtp_debug()  ### для отладки в консоли
        else:
            smtp_server = connect_to_smtp()

        try:
            smtp_server.sendmail(settings.sender_email, msg['To'], msg.as_string())
            logger.info('Письмо отправлено!')
        except smtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            logger.info(f'Не удалось отправить письмо. {reason}')
        smtp_server.close()


notification_sender = NotificationSender()
