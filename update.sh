#!/bin/bash
git pull
python manage.py makemigrations users blog comments
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput
supervisorctl restart leilanyu