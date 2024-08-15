import os

from celery import Celery

from config.components.celery_settings import CELERY_BROKER_URL

# Установка переменной окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра приложения Celery
app = Celery('celery_app', broker=CELERY_BROKER_URL)

# Загрузка настроек Django в Celery
app.config_from_object('django.conf:settings', namespace="CELERY")

# Автоматическое обнаружение задач (tasks) в приложениях Django
app.autodiscover_tasks()
