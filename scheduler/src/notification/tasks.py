import logging

import requests
from celery import shared_task
from celery.schedules import crontab
from requests import HTTPError

from celery_app import app
from notification.evevt_manager import TaskManager
from notification.models import NotificationType, Chanel, Notification, Status
from notification.serializers import notification_serializer

logger = logging.getLogger(__name__)


@shared_task
def task_get_new_films(task_manager: TaskManager = TaskManager()):
    try:
        new_movies = task_manager.get_new_films()
        recipients = task_manager.get_users_subscribers()
        notif_type = NotificationType.NEW_FILM.name
        # template = NotificationTemplate.objects.get(type=notif_type)

        notification = Notification.objects.create(
            title="New films",
            type=notif_type,
            channel=Chanel.EMAIL.name,
            recipients=recipients,
            # template=template,
            context=dict(film_list=new_movies)
        )
        notification_json = notification_serializer(notification)

        response = requests.post('http://app:80/api/v1/add_notification', json=notification_json)
        response.raise_for_status()

        logging.info(f'[GET_NEW_FILM] Все ок {response.json}')

    # except NotificationTemplate.DoesNotExist:
    #     logging.error(f'[GET_NEW FILM] NotificationTemplate с типом  {notif_type} не найден')
    #     raise Exception('NotificationTemplate с типом  {notif_type} не найден')
    except HTTPError as e:
        logging.error(f'[GET_NEW_FILM] При отправке произошла ошибка {e}')
        notification.status = Status.ERROR.name
        notification.save()
        raise Exception(f'При отправке произошла ошибка {e}')
    except Exception as e:
        logging.error(f'[GET_NEW FILM] Видимо что-то случилось {e}')
        raise Exception(f'Видимо что-то случилось {e}')


@shared_task
def task_get_new_episodes_of_series(task_manager: TaskManager = TaskManager()):
    try:
        new_episodes = task_manager.get_new_episode_of_series()

        for episode in new_episodes:
            user_group = episode.pop('users')
            episode_number = episode.pop('episode_number')
            notif_type = NotificationType.NEW_EPISODE.name
            # template = NotificationTemplate.objects.get(type=notif_type)
            message = f'Вышел новый эпизод {episode_number}  сериала {episode['title']}'

            notification = Notification.objects.create(
                title='New episode of series',
                type=notif_type,
                channel=Chanel.EMAIL.name,
                user_group=user_group,
                # template=template,
                context=dict(film_list=[episode,], episode_number=episode_number, message=message)
            )
            notification_json = notification_serializer(notification)

            response = requests.post('http://app:80/api/v1/add_notification', json=notification_json)
            response.raise_for_status()

            logging.info(f'[GET_NEW_EPISODE] Все ок {response.json}')

            notification.status = Status.SENT.name
            notification.save()
    # except NotificationTemplate.DoesNotExist:
    #     logging.error(f'[GET_NEW GET_NEW_EPISODE] NotificationTemplate с типом {notif_type} не найден')
    #     raise Exception('NotificationTemplate с типом  {notif_type} не найден')
    except HTTPError as e:
        logging.error(f'[GET_NEW_EPISODE] При отправке произошла ошибка {e}')
        notification.status = Status.ERROR.name
        notification.save()
        raise Exception(f'При отправке произошла ошибка {e}')
    except Exception as e:
        logging.error(f'[GET_NEW_EPISODE] Видимо что-то случилось {e}')
        raise Exception(f'Видимо что-то случилось {e}')


@shared_task
def task_send_admin_notification(notification_id: int):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification_json = notification_serializer(notification)

        response = requests.post('http://app:80/api/v1/add_notification', json=notification_json)
        response.raise_for_status()

        logging.info(f'[ADMIN_NOTIFICATION] Все ок {response.json}')

        notification.status = Status.SENT.name
        notification.save()
    except Notification.DoesNotExist:
        logging.error(f'[ADMIN_NOTIFICATION] Notification с id {notification_id} не найден')
        raise Exception('Notification с id {notification_id} не найден')
    except HTTPError as e:
        logging.error(f'[ADMIN_NOTIFICATION] При отправке произошла ошибка {e}')
        notification.status = Status.ERROR.name
        notification.save()
        raise Exception(f'При отправке произошла ошибка {e}')
    except Exception as e:
        logging.error(f'[ADMIN_NOTIFICATION] Видимо что-то случилось {e}')
        raise Exception(f'Видимо что-то случилось {e}')


@app.on_after_finalize.connect
def periodic_task_notification_new_movies(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='0', hour='18', day_of_week='fri'),  # 18:00 по пятницам
        task_get_new_films.s(),
        name='New movies friday evening',
    )


@app.on_after_finalize.connect
def periodic_task_notification_new_episodes(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='0', hour='12'),  # 12:00
        task_get_new_episodes_of_series.s(),
        name='New episodes of series daily',
    )

# schedule, created = CrontabSchedule.objects.get_or_create(hour=12, minute=0)
#
# PeriodicTask.objects.create(
#     crontab=schedule,
#     name='New episodes of series daily',
#     task='your_app.tasks.task_get_new_episodes_of_series',
# )
