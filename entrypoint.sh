#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

# echo "Downloading cities_light data and importing to DB..."
# python manage.py cities_light -v 1 --progress

echo "DB upgraded"
exec "$@"