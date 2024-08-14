class TaskManager:
    def get_new_films(self, service: MockService = MockService()):
        """
        Предполагаем, что у сервиса поиска фильмов есть метод get_new_films,
        возвращающий список новых фильмов.
        """
        new_films = service.get_new_films()
        return new_films

    def get_bookmarks(self, service: MockService = MockService()):
        pass
