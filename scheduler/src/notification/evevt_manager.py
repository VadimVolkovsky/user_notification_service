class MockService:

    def __init__(self, batch_num: int = 2, batch_size: int = 3):
        self.batch_num = batch_num
        self.batch_size = batch_size

    def get_bookmarks(self) -> iter:
        for _ in range(self.batch_num):
            batch = [
                {'content': {'bookmarks': {}}, 'user_id': uuid.uuid4()}
                for _ in range(self.batch_size)
            ]
            yield batch

    def get_stats(self) -> iter:
        for _ in range(self.batch_num):
            batch = [
                {'content': {'stats': {}}, 'user_id': uuid.uuid4()}
                for _ in range(self.batch_size)
            ]
            yield batch

    def get_new_films(self) -> dict:
        return {}

class NewFilms:

    def __init__(self, service):
        self.service = service

    def get_new_films(self) -> list:
        """
        Предполагаем, что у сервиса поиска фильмов есть метод get_new_films,
        возвращающий список новых фильмов.
        """
        return self.service.get_new_films()

    def create_notification(self) -> NoveltiesMessage:
        """
        Преобразование полученных от сервиса поиска фильмов данных
        в готовое для отправки в брокер сообщение.
        """
        return NoveltiesMessage(status=Statuses.PREPARED, content={'films': self.get_new_films()})
