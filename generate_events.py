import random
import time
from datetime import datetime

import faker
import requests

faker = faker.Faker()


NUMBER_OF_EVENTS = 50
NOTIFICATION_SERVICE_URL = 'http://localhost:8000/api/v1/add_notification'


def generate_new_user_registration() -> dict:
    """Создание события регистрации нового пользователя"""
    event = {
        "type": "new_user",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "urgent": True,
        "payload": {
            "user_id": faker.uuid4(),
        }
    }
    return event


def generate_new_series() -> dict:
    """Создание события выхода новой серии сериала"""
    event = {
        "type": "new_series",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "urgent": True,
        "payload": {
            "film_id": faker.uuid4(),
        }
    }
    return event


def generate_new_like_for_review() -> dict:
    """Создание события добавления нового лайка на ревью"""
    event = {
        "type": "new_like_review",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "urgent": False,
        "payload": {
            "user_id": faker.uuid4(),
            "review_id": faker.uuid4(),
            "score": faker.random_int(min=0, max=10),
        }
    }
    return event


def generate_news() -> dict:
    """Создание новостного события"""
    event = {
        "type": "news",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "urgent": faker.boolean(),
        "payload": {
            "top_films": [faker.uuid4() for _ in range(5)],
            "top_series": [faker.uuid4() for _ in range(5)]
        }
    }
    return event


def send_event(event: dict):
    """Функция для отправки событий в notification service"""
    requests.post(NOTIFICATION_SERVICE_URL, json=event, timeout=20)
    print(f'Отправлен event типа: {event.get("type")}')


if __name__ == "__main__":
    assert NOTIFICATION_SERVICE_URL != '', 'Укажи ссылку NOTIFICATION_SERVICE_URL'

    event_functions = [
        generate_new_user_registration,
        generate_new_series,
        generate_new_like_for_review,
        generate_news
    ]

    for _ in range(NUMBER_OF_EVENTS):
        generate_random_event = random.choice(event_functions)
        event = generate_random_event()
        send_event(event)
        # time.sleep(1)

