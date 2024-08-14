import logging

import requests
from celery.schedules import crontab

from scheduler.src.celery import app
from scheduler.src.notification.evevt_manager import TaskManager
from scheduler.src.notification.models import NotificationType, Chanel, NotificationTemplate, Notification
from scheduler.src.notification.serializers import notification_serializer

logger = logging.getLogger(__name__)


@app.task
def task_get_new_films(task_manager: TaskManager = TaskManager()):
    try:
        new_movies = task_manager.get_new_films()
        user_group = task_manager.get_users_subscribers()
        notif_type = NotificationType.NEW_FILM.name
        template = NotificationTemplate.objects.get(type=notif_type)

        notification = Notification.objects.create(
            title="New films",
            type=NotificationType.NEW_FILM.name,
            channel=Chanel.EMAIL.name,
            user_group=user_group,
            template=template,
            context=dict(film_list=new_movies)
        )
        notification_json = notification_serializer(notification)

        response = requests.post('http://app:8000/api/v1/add_event', json=notification_json)
        logging.info(f'[GET_NEW FILM] Все ок {response.json}')
    except NotificationTemplate.DoesNotExist:
        logging.error(f'[GET_NEW FILM] NotificationTemplate с типом  {notif_type} не найден')
        raise Exception('NotificationTemplate с типом  {notif_type} не найден')
    except Exception as e:
        logging.error(f'[GET_NEW FILM] Видимо что-то случилось {e}')
        raise Exception(e)


@app.on_after_configure.connect
def periodic_task_notification_new_movies(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=18, day_of_week='fri'),  # 18:00 по пятницам,
        task_get_new_films.s(),
        name='New movies',
    )
