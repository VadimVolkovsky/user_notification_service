import smtplib

from core.config import settings


def connect_to_smtp():
    """Метод для подключения к SMTP серверу"""
    server = smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port)
    server.login(settings.sender_login, settings.sender_password)
    return server


def connect_to_smtp_debug():
    """
    Метод для отладки отправки сообщений - сообщения отправляются в консоль.
    Перед использованием необходимо запустить локальный почтовый сервер:
    sudo python -m smtpd -n -c DebuggingServer localhost:25
    """
    server = smtplib.SMTP(settings.smtp_server_debug, settings.smtp_port_debug)
    return server
