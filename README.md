### Backend for Real-estate rent review system

![Build Status](https://github.com/m0nk-tnd/real-estate-review-system-be/actions/workflows/ci.yml/badge.svg?branch=develop)

To start the project using Docker you should use commands (from project folder):
docker-compose build
docker-compose up -d

To start the project locally you should run the 
prepare_venv.sh
 script, then execute commands
python manage.py migrate
 and 
python manage.py cities_light
 to download django-cities-light data.

To test the project with fixtures you should use 
$ python manage.py loaddata fixtures/*.json
 to load first data.

## Available URLs

All available urls are presented here

### Admin

Method | URL | Description 
------|------|-------
GET | */admin* | Панель администратора


**Note**: further all urls must have the prefix `/api/v1/` (e.g. */api/v1/reviews/tenant*)


### Authentication

Method | URL | Description 
------|------|-------
POST | */login* | Получение JWT токена для авторизации
POST | */refresh* | Обновление JWT токена для авторизации
POST | */register* | Регистрация


### Reviews

*subject*: `tenant` or `landlord`

Method | URL | Description 
------|------|-------
GET | */reviews/{subject}* | Получение списка отзывов
POST | */reviews/{subject}* | Создание отзыва
GET | */reviews/{subject}/{review_id}* | Получение отзыва по id
PATCH | */reviews/{subject}/{reviews_id}* | Изменение отзыва по id
DELETE | */reviews/{subject}/{review_id}* | Удаление отзыва по id


### Properties

Method | URL | Description 
------|------|-------
GET | */properties* | Получение списка собственностей
POST | */properties* | Создание собственности
GET | */properties/{property_id}* | Получение собственности по id
PATCH | */properties/{property_id}* | Изменение собственности по id
DELETE | */properties/{property_id}* | Удаление собственности по id


### Profiles

*subject*: `tenant` or `landlord`

Method | URL | Description 
------|------|-------
GET | */profiles/{subject}* | Получение списка профилей 
POST | */profiles/{subject}* | Создание профиля
GET | */profiles/{subject}/{profile_id}* | Получение профиля по id
PATH | */profiles/{subject}/{profile_id}* | Изменение профиля по id
DELETE | */profiles/{subject}/{profile_id}* | Удаление профиля по id


### Notifications

Method | URL | Description 
------|------|-------
GET | */notifications* | Получение списка уведомлений пользователя
GET | */notifications/templates* | Получение шаблонов уведомлений пользователя
