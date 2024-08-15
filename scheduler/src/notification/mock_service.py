import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()


class MockService:
    def generate_new_films(self) -> list[dict]:

        movies = []
        for _ in range(5):
            movie = {
                "id": str(uuid.uuid4()),
                "title": fake.catch_phrase(),
                "release": (datetime.now() - timedelta(days=fake.random_int(min=0, max=7))).strftime('%Y-%m-%d')
            }
            movies.append(movie)
        return movies

    def get_bookmarks(self) -> iter:
        pass

    def get_new_films(self) -> list[dict]:
        return self.generate_new_films()

    def get_new_episodes_of_series(self) -> list[dict]:
        return self.generate_new_episodes_of_series()

    def generate_new_episodes_of_series(self) -> list[dict]:
        series_list = []
        for _ in range(5):
            series = {
                'id': str(uuid.uuid4()),
                'title': fake.catch_phrase(),
                'release': (datetime.now() - timedelta(days=fake.random_int(min=0, max=7))).strftime('%Y-%m-%d'),
                'episode_number': fake.random_int(min=0, max=20),
                'users': [str(uuid.uuid4()) for _ in range(fake.random_int(min=1, max=5))]
            }
            series_list.append(series)

        return series_list
