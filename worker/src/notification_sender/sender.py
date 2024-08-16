import os
import logging
import smtplib
from email.message import EmailMessage
from functools import lru_cache

from jinja2 import FileSystemLoader, Environment

from core.config import settings
from notification_sender.smtp import connect_to_smtp, connect_to_smtp_debug
from schemas.models import NotificationToSend, Recipient

logger = logging.getLogger("__name__")


class NotificationSender:
    """Класс для подготовки и отправки уведомления пользователю"""

    def __init__(self):
        self._loader = FileSystemLoader(searchpath=f'{os.path.dirname(__file__)}/templates')
        self.env = Environment(loader=self._loader)

    def _create_email_notification(self, recipient: Recipient, notification: NotificationToSend) -> EmailMessage:
        """Подготовка уведомления для отправки по email"""
        email_data = {
            "greeting": f"Привет {recipient.name} !",
            "message": notification.context.message,
            "sender_name": settings.sender_name,
        }

        message = EmailMessage()
        message['From'] = settings.sender_email
        message['To'] = recipient.email
        message['Subject'] = notification.title

        template = self.env.get_template(f'{notification.type}.html')
        output = template.render(**email_data)
        message.add_alternative(output, subtype='html')
        return message

    def _prepare_emails(self, notification: NotificationToSend) -> list[EmailMessage]:
        """Метод для подготовки сообщений для отправки"""
        msgs = []
        for recipient in notification.recipients:
            msgs.append(self._create_email_notification(recipient, notification))
        return msgs

    @staticmethod
    def _get_smtp_server():
        if settings.debug:
            smtp_server = connect_to_smtp_debug()  ### для отладки в консоли
        else:
            smtp_server = connect_to_smtp()
        return smtp_server

    def send_notification_by_email(self, notification: NotificationToSend):
        """Отправка уведомления пользователю по email"""
        msgs = self._prepare_emails(notification)
        if not msgs:
            print('Нет сообщений для отправки')
            return

        smtp_server = self._get_smtp_server()
        for msg in msgs:
            try:
                smtp_server.sendmail(settings.sender_email, msg['To'], msg.as_string())
                print('Письмо отправлено!')
            except smtplib.SMTPException as exc:
                reason = f'{type(exc).__name__}: {exc}'
                print(f'Не удалось отправить письмо. {reason}')
        smtp_server.close()


@lru_cache()
def get_sender() -> NotificationSender:
    return NotificationSender()
