from notification.mock_service import MockService


class TaskManager:
    def get_new_films(self, service: MockService = MockService()):
        """
        Предполагаем, что у сервиса поиска фильмов есть метод get_new_films,
        возвращающий список новых фильмов.
        """
        new_films = service.get_new_films()
        return new_films

    def get_new_episode_of_series(self, service: MockService = MockService()):
        """
        Предполагаем, что у сервиса поиска фильмов есть метод get_new_films,
        возвращающий новых серий для сериалов.
        """
        new_episodes = service.get_new_episodes_of_series()
        return new_episodes

    def get_bookmarks(self, service: MockService = MockService()):
        pass
