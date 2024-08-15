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


(check)
 Сгенерировать рандомные события 
```
docker exec notification_service_app python generate_events.py
```


### Документация API
```
http://localhost:8000/api/openapi
```