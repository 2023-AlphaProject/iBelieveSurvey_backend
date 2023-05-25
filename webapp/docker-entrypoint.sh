#!/bin/bash
python manage.py makemigrations --noinput

python manage.py migrate --noinput
python manage.py template_objs_in_db

python manage.py collectstatic --noinput -v 0

gunicorn config.wsgi:application --env DJANGO_SETTINGS_MODULE=config.settings.local --bind 0.0.0.0:8000