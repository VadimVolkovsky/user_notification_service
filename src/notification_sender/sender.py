import os
import smtplib
from email.message import EmailMessage

from jinja2 import FileSystemLoader, Environment

from notification_sender.smtp_config import connect_to_smtp, sender_email
from schemas.api_schemas import Notification, Recipient


class NotificationSender:
    """Класс для подготовки и отправки уведомления пользователю"""

    @staticmethod
    def _create_new_user_notification(recipient: Recipient, notification: Notification) -> EmailMessage:
        """Подготовка уведомления о регистрации нового пользователя"""
        email_data = {
            "subject": notification.title,
            "greeting": f"Привет {recipient.name} !",
            "message": notification.context['message'],
            "sender_name": "Онлайн Кинотеатр Практикум",
        }

        message = EmailMessage()
        message['From'] = sender_email
        message['To'] = recipient.email
        message['Subject'] = 'Привет!'

        # Указываем расположение шаблонов
        current_path = f'{os.path.dirname(__file__)}/templates'
        loader = FileSystemLoader(current_path)
        env = Environment(loader=loader)
        template = env.get_template('email_template.html')

        output = template.render(**email_data)
        message.add_alternative(output, subtype='html')
        return message

    def _prepare_emails(self, notification: Notification) -> list[EmailMessage]:
        """Метод для подготовки сообщений для отправки в зависимости от типа события"""
        msgs = []
        if notification.type == 'new_user':
            for recipient in notification.recipients:
                msgs.append(self._create_new_user_notification(recipient, notification))
        elif notification.type == 'new_series':
            print('Уведомление о новых сериях пока не поддерживается')
            pass
        return msgs

    def send_notification(self, notification: Notification):
        """Отправка уведомления пользователю"""
        msgs = self._prepare_emails(notification)
        if not msgs:
            print('Нет сообщений для отправки')
            return

        # smtp_server = connect_to_smtp_debug()  # TODO для отладки в консоли
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

#
# ### TODO DEBUG тест отправки сообщений:
# notification_to_send_example_1 = NotificationToSend(
#     type='new_user',
#     subject='Регистрация в Онлайн Кинотеатре',
#     message='Добро пожаловать в онлайн кинотеатр Практикум',
#     payload=[
#         {
#             'email': 'vadimas29@yandex.ru',
#             'name': 'Vadim',
#         }
#     ]
# )
#
# notification_to_send_example_2 = NotificationToSend(
#     type='new_series',
#     subject='Новая серия "Ходячие Мертвецы"',
#     message='Привет, на платформе вышла новая серия',
#     payload=[
#         {
#             'email': 'vadimas29@yandex.ru',
#             'name': 'Ivan',
#         },
#         {
#             'email': 'vadimas29@yandex.ru',
#             'name': 'Dmitry',
#         }
#     ]
# )
#
# notification_sender.send_notification(notification_to_send_example_1)
