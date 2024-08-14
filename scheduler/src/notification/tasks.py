import requests
from celery import shared_task

@shared_task
def fetch_and_send_movies():
    # Получение списка новых фильмов с исходного API
    response = requests.get('https://source-api.example.com/new-movies')

    if response.status_code == 200:
        movies = response.json()

        # Отправка списка на целевой API
        destination_response = requests.post('https://destination-api.example.com/movies', json=movies)
        if destination_response.status_code == 200:
            return 'Фильмы успешно отправлены!'
        else:
            return f'Не удалось отправить фильмы: {destination_response.status_code}'
    else:
        return f'Не удалось получить фильмы: {response.status_code}'
