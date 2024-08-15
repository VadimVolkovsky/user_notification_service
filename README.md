# Проектная работа 10 спринта

Сервис уведомлений

Ссылка на [репозиторий](https://github.com/VadimVolkovsky/notifications_sprint_1)



### Запуск проекта


Скопировать .env
```
cp .env_example .env
```

Собрать и запустить контейнеры
```
docker compose up -d
```


Сгенерировать события new_user
```
docker exec notification_service_app python generate_events.py
```


### Документация API
```
http://127.0.0.1:8000/api/openapi
```

### Админка
```
http://127.0.0.1:8001/admin/
```

Создание супер-юзера
```
make createsuperuser
```

