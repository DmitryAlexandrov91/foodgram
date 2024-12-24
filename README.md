![Main Foodgram Workflow](https://github.com/DmitryAlexandrov91/foodgram/actions/workflows/main.yml/badge.svg)

# Foodgram

Foodgram - выпускной проект Яндекс курса python-разработчик. Построен на взаимодействии api с JavaScript фронтендем.
Функционал приложения позволяет просматривать и выкладывать рецепты разнообразных блюд, созданных на базе более 2000 подготовленных ингредиентов!
Регистрируйтесь и выкладывайте свои кулинарные шедевры. Ваш путь до шеф-повара начинается именно здесь!


## Функции приложения

- Регистрация и аутентификация пользователей, установка аватара
- Загрузка фотографий рецептов с возможностью добавления описания
- Просмотр рецептов других пользователе
- Возможность подписываться на других пользователей
- Добавление понравившихся рецептов в избранное и корзину покупок
- Возможность скачать корзину покупок.

## Стек технологий

### Backend

- Python(Django, Django REST Framework, Djoser)
- PostgreSQL (база данных)
- Gunicorn (WSGI-сервер)
- Nginx

### Frontend

- HTML/CSS
- JavaScript (ES6+)
- Bootstrap (CSS-фреймворк)

### Инструменты разработки

- Docker (контейнеризация)
- Git (система контроля версий)

## Развертывание проекта

1. Клонируйте репозиторий:

   
   git clone https://github.com/DmitryAlexandrov91/foodgram.git
   

2. Перейдите в директорию проекта:

   
   cd foodgram
   

3. Запустите контейнеры с помощью Docker Compose:

   
   docker-compose up -d

4. Выполнить следующие команды внутри запущенного контейнера backend:
 - docker compose -f docker-compose.yml exec backend python manage.py migrate
 - docker compose -f docker-compose.yml exec backend python manage.py collectstatic
 - docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/

Заполните базу данных подготовленным компанией Яндекс списком ингредиетов(более 2000 наименований!):
 - docker compose -f docker-compose.yml exec backend python manage.py get_data data/ingredient.csv

Для удобства так же подготовлены 4 тега (завтрак, обед, ужин, перекус)
 - docker compose -f docker-compose.yml exec backend python manage.py get_data data/tag.csv


Если вы работаете по системой Linux или MacOs не забывайте добавлять в начало команда sudo.

После успешного запуска контейнеров приложение будет доступно по адресу http://localhost:9090/

## Настройка переменных окружения (.env)

Создайте файл .env в корневой директории проекта и добавьте следующие переменные:

- POSTGRES_DB=foodgram
- POSTGRES_USER=foodgram_user
- POSTGRES_PASSWORD=foodgram_password
- DB_NAME=foodgram
- DB_HOST=db
- DB_PORT=5432
- SECRET_KEY = секретный код проекта
- DEBUG = запуск проекта в режиме отладки 'True' или 'False'  
- ALLOWED_HOSTS = Строка из URL адресов проекта через запятую. Например 'ya.ru, 89.899.899.89'

## Автор

Александров Дмитрий Александрович

<u>GitHub</u>
 - https://github.com/DmitryAlexandrov91

