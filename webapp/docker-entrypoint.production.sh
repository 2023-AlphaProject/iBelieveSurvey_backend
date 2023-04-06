#!/bin/bash
python manage.py makemigrations --noinput

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn config.wsgi:application --env DJANGO_SETTINGS_MODULE=config.settings.production --bind 0.0.0.0:8000