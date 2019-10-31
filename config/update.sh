#!/bin/bash
python manage.py makemigrations users blog comments
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput
# python manage.py runserver 0.0.0.0:8080