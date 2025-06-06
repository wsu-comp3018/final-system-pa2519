#!/bin/sh

# Wait for MariaDB to be ready
echo "Waiting for mariadb..."
while ! nc -z mariadb 3306; do
  sleep 1
done
echo "MariaDB is up!"

# Run migrations
pipenv run python manage.py makemigrations --no-input
pipenv run python manage.py migrate --no-input
pipenv run python manage.py loaddata templates.json

# Start Gunicorn server
pipenv run gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4