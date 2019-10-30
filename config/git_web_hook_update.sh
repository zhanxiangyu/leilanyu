# unset GIT_DIR

cd /home/leilanyu
git pull origin dev
/root/.virtualenvs/leilanyu/bin/pip install -r requirements.txt
/root/.virtualenvs/leilanyu/bin/python manage.py makemigrations
/root/.virtualenvs/leilanyu/bin/python manage.py migrate
/root/.virtualenvs/leilanyu/bin/python manage.py compilemessages
/root/.virtualenvs/leilanyu/bin/python manage.py collectstatic --noinput
supervisorctl restart all
