# unset GIT_DIR

cd /home/leilanyu
git pull origin dev
/root/.virtualenvs/leilanyu/bin/pip install -r requirements.txt
supervisorctl restart all
