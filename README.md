### Backend for Real-estate rent review system

![Build Status](https://github.com/m0nk-tnd/real-estate-review-system-be/actions/workflows/ci.yml/badge.svg?branch=develop)

To start the project using Docker you should use commands (from project folder):
```
docker-compose build
docker-compose up -d
```

To start the project locally you should run the ```prepare_venv.sh``` script, then execute commands
```python manage.py migrate``` and ```python manage.py cities_light``` to download django-cities-light data.

To test the project with fixtures you should use ```$ python manage.py loaddata fixtures/*.json``` to load first data.

