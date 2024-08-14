import os
import smtplib
from email.message import EmailMessage

from jinja2 import FileSystemLoader, Environment

from notification_sender.smtp_config import connect_to_smtp, sender_email
from schemas.api_schemas import NotificationToSend, Recipient, Context


class NotificationSender:
    """Класс для подготовки и отправки уведомления пользователю"""

    @staticmethod
    def _create_new_user_notification(recipient: Recipient, notification: NotificationToSend) -> EmailMessage:
        """Подготовка уведомления о регистрации нового пользователя"""
        email_data = {
            "subject": notification.title,
            "greeting": f"Привет {recipient.name} !",
            "message": notification.context.message,
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
        template = env.get_template(f'{notification.type}.html')

        output = template.render(**email_data)
        message.add_alternative(output, subtype='html')
        return message

    def _prepare_emails(self, notification: NotificationToSend) -> list[EmailMessage]:
        """Метод для подготовки сообщений для отправки в зависимости от типа события"""
        msgs = []
        if notification.type == 'new_user':
            for recipient in notification.recipients:
                msgs.append(self._create_new_user_notification(recipient, notification))
        elif notification.type == 'new_series':
            print('Уведомление о новых сериях пока не поддерживается') # TODO
            pass
        return msgs

    def send_notification_by_email(self, notification: NotificationToSend):
        """Отправка уведомления пользователю по email"""
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
# # ### TODO DEBUG тест отправки сообщений:
# recipient_1 = Recipient(
#     id="01276bc8-84d9-4cb4-b574-9eea25a526f9",
#     email='vadimas29@yandex.ru',
#     name='Vadim'
# )
# context = Context(message='Добро пожаловать в онлайн кинотеатр Практикум')
# notification_to_send_example_1 = NotificationToSend(
#     title='Регистрация в Онлайн Кинотеатре',
#     type='new_user',
#     recipients=[recipient_1],
#     context=context
# )
# #

# notification_sender.send_notification_by_email(notification_to_send_example_1)
