import os
import smtplib

from dotenv import load_dotenv

load_dotenv()

# TODO создать settings

### PROD config ###
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))

sender_login = os.getenv('SENDER_LOGIN')
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
sender_name = os.getenv('SENDER_NAME')


### DEBUG config (для локальной отладки) ###
smtp_server_debug = "localhost"
smtp_port_debug = 25


def connect_to_smtp():
    """Метод для подключения к SMTP серверу"""
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_login, sender_password)
    return server


def connect_to_smtp_debug():
    """
    Метод для отладки отправки сообщений - сообщения отправляются в консоль.
    Перед использованием необходимо запустить локальный почтовый сервер:
    sudo python -m smtpd -n -c DebuggingServer localhost:25
    """
    server = smtplib.SMTP(smtp_server_debug, smtp_port_debug)
    return server
