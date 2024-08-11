import smtplib

# TODO зарегать smtp сервер по теории из практикума и добавить сюда его креды:
smtp_server = "smtp.server.com"
smtp_port = 587
sender_email = "admin@online-cinema.com"
sender_password = "password"


def connect_to_smtp():
    """Метод для подключения к SMTP серверу"""
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    return server
