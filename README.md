# Foodgram

Проект — сайт «Продуктовый помощник»

## Адрес сервера: http://51.250.103.200 (superuser: admin, password: admin)

### Описание
«Продуктовый помощник» - это сайт где пользователи могут вести свой кулинарный блог добавляя рецепты, делясь ими с другими пользователями а так же подписываясь на других пользователей и добавляя рецепты в "избранное" и "список покупок".

## Стек технологий
- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- базы данны - PostgreSQL
- автоматическое развертывание проекта - Docker, docker-compose, Gunicorn, Nginx

### Запуск приложения
1. Если у вас уже установлены docker и docker-compose, этот шаг можно пропустить, иначе можно воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).
2. Собрать контейнер и запустить
```
docker-compose up -d --build
```
3. Выполнить миграцию базы данных
```
docker-compose exec backend python manage.py migrate --noinput
```
4. Собрать статические файлы
```
docker-compose exec backend python manage.py collectstatic --no-input
```
5. Остановить контейнер
```
docker-compose down
```
6. Создать суперпользователя
```
docker-compose run backend python manage.py createsuperuser
```