import os
import smtplib
from email.message import EmailMessage

from jinja2 import FileSystemLoader, Environment

from notification_sender.smtp_config import connect_to_smtp, sender_email
from schemas.api_schemas import NotificationToSend


class NotificationSender:
    """Класс для подготовки и отправки уведомления пользователю"""

    @staticmethod
    def _create_new_user_notification(user: dict, notification: NotificationToSend) -> EmailMessage:
        """Подготовка уведомления о регистрации нового пользователя"""
        email_data = {
            "subject": notification.subject,
            "greeting": f"Привет {user['name']} !",
            "message": notification.message,
            "sender_name": "Онлайн Кинотеатр Практикум",
        }

        message = EmailMessage()
        message['From'] = sender_email
        message['To'] = user["email"]
        message['Subject'] = 'Привет!'

        # Указываем расположение шаблонов
        current_path = f'{os.path.dirname(__file__)}/templates'
        loader = FileSystemLoader(current_path)
        env = Environment(loader=loader)
        template = env.get_template('email_template.html')

        output = template.render(**email_data)
        message.add_alternative(output, subtype='html')
        return message

    def _prepare_email(self, notification: NotificationToSend) -> EmailMessage | None:
        """Метод для подготовки email в зависимости от типа события"""
        if notification.type == 'new_user':
            for user in notification.payload:
                return self._create_new_user_notification(user, notification)
        elif notification.type == 'new_series':
            pass
        print('Уведомления для других типов событий еще не поддерживаются')
        return

    def send_notification(self, notification: NotificationToSend):
        """Отправка уведомления пользователю"""

        msg = self._prepare_email(notification)
        if not msg:
            return

        # smtp_server = connect_to_smtp_debug()  # TODO для отладки в консоли
        smtp_server = connect_to_smtp()
        try:
            smtp_server.sendmail(sender_email, msg['To'], msg.as_string())
        except smtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            print(f'Не удалось отправить письмо. {reason}')
        else:
            print('Письмо отправлено!')
        finally:
            smtp_server.close()


notification_sender = NotificationSender()


### TODO DEBUG тест отправки сообщений:
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
#             'email': 'user_1@mail.ru',
#             'name': 'Ivan',
#         },
#         {
#             'email': 'user_2@mail.ru',
#             'name': 'Dmitry',
#         }
#     ]
# )
#
# notification_sender.send_notification(notification_to_send_example_1)
