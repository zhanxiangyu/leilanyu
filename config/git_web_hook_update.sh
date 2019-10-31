# unset GIT_DIR
root_path=/home/leilanyu
pip_path=/root/.virtualenvs/leilanyu/bin/pip
python_path=/root/.virtualenvs/leilanyu/bin/python

cd $root_path
git pull origin dev
supervisorctl stop leilanyu
$pip_path install -r requirements.txt
$python_path manage.py makemigrations
$python_path manage.py migrate
$python_path manage.py compilemessages
$python_path manage.py collectstatic --noinput
supervisorctl start leilanyu
echo 'over'

