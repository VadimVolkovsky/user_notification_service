import os
import smtplib
from email.message import EmailMessage

from jinja2 import FileSystemLoader, Environment

from smtp_config import connect_to_smtp, sender_email, sender_name
from schemas.api_schemas import NotificationToSend, Recipient


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
            "sender_name": sender_name,
        }

        message = EmailMessage()
        message['From'] = sender_email
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

    def send_notification_by_email(self, notification: NotificationToSend):
        """Отправка уведомления пользователю по email"""
        msgs = self._prepare_emails(notification)
        if not msgs:
            print('Нет сообщений для отправки')
            return

        # smtp_server = connect_to_smtp_debug()  ### для отладки в консоли
        smtp_server = connect_to_smtp()
        for msg in msgs:
            try:
                smtp_server.sendmail(sender_email, msg['To'], msg.as_string())
                print('Письмо отправлено!')
            except smtplib.SMTPException as exc:
                reason = f'{type(exc).__name__}: {exc}'
                print(f'Не удалось отправить письмо. {reason}')
        smtp_server.close()


notification_sender = NotificationSender()


#### TODO DEBUG тест отправки сообщений:

### TODO Регистрация нового пользователя
# recipient_1 = Recipient(
#     id="01276bc8-84d9-4cb4-b574-9eea25a526f9",
#     email='vadimas29@yandex.ru',
#     name='Vadim'
# )
# context = Context(message='Добро пожаловать в онлайн кинотеатр Практикум')
# notification_new_user = NotificationToSend(
#     title='Регистрация в Онлайн Кинотеатре',
#     type='new_user',
#     recipients=[recipient_1],
#     context=context
# )
# #

# ### TODO Выход нового эпизода
# recipient_1 = Recipient(
#     id="01276bc8-84d9-4cb4-b574-9eea25a526f9",
#     email='vadimas29@yandex.ru',
#     name='Vadim'
# )
# recipient_2 = Recipient(
#     id="01276bc8-84d9-4cb4-b574-9eea25a526f9",
#     email='vadimas29@yandex.ru',
#     name='Ivan'
# )
#
# context = Context(message='Вышел эпизод #5 для сериала "Ходячие Мертвецы"')
# notification_new_episode = NotificationToSend(
#     title='Новый эпизод',
#     type='new_episode',
#     recipients=[recipient_1, recipient_2],
#     context=context
# )
#
#
# notification_sender.send_notification_by_email(notification_new_episode)
