import uuid
from faker import Faker
from datetime import datetime, timedelta


class MockService:
    def generate_new_films(self) -> list[dict]:
        fake = Faker()

        movies = []
        for _ in range(5):
            movie = {
                "id": str(uuid.uuid4()),
                "title": fake.sentence(nb_words=3),
                "release": (datetime.now() - timedelta(days=fake.random_int(min=0, max=7))).strftime('%Y-%m-%d')
            }
            movies.append(movie)
            return movies

    def get_bookmarks(self) -> iter:
        pass

    def get_new_films(self) -> list[dict]:
        return self.generate_new_films()
