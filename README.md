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

Применить миграции alembic
```
docker exec notification_service_app alembic upgrade head
```



### Документация API
```
http://localhost:8000/api/openapi
```