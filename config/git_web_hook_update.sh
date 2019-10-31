# unset GIT_DIR

cd /Users/zhan/projects/leilanyu
git pull origin dev
/root/.virtualenvs/leilanyu/bin/pip install -r requirements.txt
supervisorctl stop leilanyu
/root/.virtualenvs/leilanyu/bin/python manage.py makemigrations
/root/.virtualenvs/leilanyu/bin/python manage.py migrate
/root/.virtualenvs/leilanyu/bin/python manage.py compilemessages
/root/.virtualenvs/leilanyu/bin/python manage.py collectstatic --noinput
supervisorctl start leilanyu
echo 'over'

