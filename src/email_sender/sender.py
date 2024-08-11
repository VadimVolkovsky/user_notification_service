from jinja2 import Template


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email_sender.smtp_config import connect_to_smtp, sender_email
from schemas.api_schemas import NotificationToSend


def _create_new_user_notification(notification: NotificationToSend) -> MIMEMultipart:
    """Подготовка уведомления о регистрации нового пользователя"""
    with open("templates/email_template.html", "r") as file:
        template_str = file.read()
    email_template = Template(template_str)

    email_data = {
        "subject": "Регистрация в онлайн кинотеатре",
        "greeting": f"Привет {notification.payload['name']} !",
        "message": "Добро пожаловать в мир кино.",
        "sender_name": "Онлайн Кинотеатр Практикум",
    }
    email_content = email_template.render(email_data)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = notification.payload["email"]
    msg["Subject"] = email_data["subject"]

    # Прикрепляем HTML контент к емейлу
    msg.attach(MIMEText(email_content, "html"))
    return msg


def prepare_email(notification: NotificationToSend) -> MIMEMultipart | None:
    """Метод для подготовки email в зависимости от типа события"""
    if notification.type == 'new_user':
        return _create_new_user_notification(notification)
    elif notification.type == 'new_series':
        pass
    print('Уведомления для других типов событий еще не поддерживаются')
    return


def send_notification(notification: NotificationToSend):
    """Отправка уведомления пользователю"""
    smtp_server = connect_to_smtp()
    msg = prepare_email(notification)
    if not msg:
        smtp_server.quit()

    print(f"Отправляем письмо на адрес {notification.payload['email']}")
    smtp_server.sendmail(sender_email, notification.payload["email"], msg.as_string())
    smtp_server.quit()


if __name__ == "__main__":
    send_notification()


