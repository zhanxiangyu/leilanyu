#!/bin/bash
# 一次项目部署安装脚本

echo 'ubuntu 16.04 基本环境搭建'
echo '开发环境'

# 设置变量
NAME=leilanyu
DATABASE_NAME=$NAME
PRODUCT_DIR=/home/$NAME
ENV_PATH=$HOME/.virtualenvs/$NAME
IP=106.12.72.157
WEBSITE=www.leilanyu.com
GIT_PROJECT=git@github.com:zhanxiangyu/leilanyu.git
DJAGNO_APP=(users blog comments xadmin)


# 不同源安装的nginx版本不一样 查看版本  当前安装1.10.3-0ubuntu0.16.04.3 应该没有多大区别
# sudo apt-cache madison  nginx
# 安装基础包
sudo apt-get install -y python-pip
sudo apt install -y zip
sudo apt-get install mariadb-server mariadb-client redis-server -y
# 需要配置redis 密码
sudo apt-get install libmysqlclient-dev libevent-dev -y
sudo apt-get install gettext memcached nginx -y



# pip 换源
if [ ! -d "$HOME/.pip/" ]; then
mkdir $HOME/.pip/
cat <<EOF >> $HOME/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
EOF

else
echo $HOME'/.pip/ 目录已经存在'
fi


# 安装python虚拟环境， 和supervisor进程控制
pip install virtualenv
pip install virtualenvwrapper
pip install supervisor==3.3.5


if [ `grep -c "WORKON_HOME" $HOME/.bashrc` -eq 0 ]; then
cat <<"EOF" >> $HOME/.bashrc
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
EOF
source $HOME/.bashrc
else
    echo "Found WORKON_HOME in $HOME/.bashrc ."
fi


# supervisor配置文件
if [ ! -f "/etc/supervisord.conf" ]; then
cd /tmp
echo_supervisord_conf > supervisord.conf
cat <<EOF >> supervisord.conf
[include]
files = /etc/supervisord.d/*.conf
EOF
mv supervisord.conf /etc/
mkdir /etc/supervisord.d/
fi


# git下载项目
if [ ! -d $PRODUCT_DIR ]; then
cd /home/ && git clone $GIT_PROJECT
else
echo '项目文件已经存在'
fi

# 进入虚拟环境
if [ ! -d "$ENV_PATH" ]; then
virtualenv -p /usr/bin/python2.7 $ENV_PATH
source $ENV_PATH/bin/activate
# mkvirtualenv $NAME
# workon $NAME
else
echo '进入虚拟环境'
# workon $NAME
source $ENV_PATH/bin/activate
fi

# 安装项目依赖包
pip install uwsgi==2.0.18
cd ${PRODUCT_DIR}
pip install -r requirements.txt



# 创建数据库
mysql -e "use ${DATABASE_NAME};"
if [ $? -eq 0 ]; then
echo "$DATABASE_NAME databases is exists"
else
echo '新建数据库'
mysql -e "
CREATE USER '${DATABASE_NAME}'@'%' IDENTIFIED BY '${DATABASE_NAME}';
CREATE USER '${DATABASE_NAME}'@'localhost' IDENTIFIED BY '${DATABASE_NAME}';
CREATE DATABASE ${DATABASE_NAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${DATABASE_NAME}'@'%';
GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${DATABASE_NAME}'@'localhost';
"
fi


# 添加该项目的私有配置
if [ -f "$PRODUCT_DIR/private_key.py" ]; then
echo 'private_key.py 文件已经配置'
else
cat <<EOF >> $PRODUCT_DIR/private_key.py
PRIVATE_JSON = {
    "DEBUG": False,
    "ALLOWED_HOSTS": ["*"],
    "DB_NAME": 'leilanyu',
    "DB_USER": "leilanyu",
    "DB_PASSWORD": "leilanyu",
    "ADMIN_URL": "admin",
}
EOF
fi

for i in ${DJAGNO_APP[*]}; do
python manage.py makemigrations $i
done

python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput


# 退出虚拟环境
deactivate

# 配置nginx文件
cd $PRODUCT_DIR
cat <<EOF >> $PRODUCT_DIR/${NAME}_nginx.conf
# mysite_nginx.conf

# the upstream component nginx needs to connect to
upstream django {
    server unix://$PRODUCT_DIR/${NAME}.sock; # for a file socket
    # server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name $IP; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias $PRODUCT_DIR/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias $PRODUCT_DIR/collectedstatic; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     $PRODUCT_DIR/uwsgi_params; # the uwsgi_params file you installed
    }
}

EOF

# 删除nginx多余的80端口占用
rm -rf /etc/nginx/sites-available/default
rm -rf /etc/nginx/sites-enabled/default

# 关联nginx
sudo ln -s $PRODUCT_DIR/leilanyu_nginx.conf /etc/nginx/sites-enabled/

# 修改nginx主配置文件 用户未root
sed -i 's/www-data/root/' /etc/nginx/nginx.conf

# copy uwsgi_params文件
cp /etc/nginx/uwsgi_params $PRODUCT_DIR/

# uwsgi启动时需要使用config文件夹，但是不会自动创建该文件夹
# 已经注入到git项目中
if [ ! -d "$PRODUCT_DIR/config" ]; then
mkdir config
fi

# 配置_uwsgi.ini文件
cat <<EOF >> $PRODUCT_DIR/${NAME}_uwsgi.ini
# mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = $PRODUCT_DIR
# Django's wsgi file
module          = ${NAME}.wsgi
# the virtualenv (full path)
home            = $ENV_PATH

# process-related settings
# master
master          = true
# maximum number of worker processes  服务器配置越好数量越高 1一核两个
processes       = 2
# the socket (use the full path to be safe
socket          = $PRODUCT_DIR/${NAME}.sock
# ... with appropriate permissions - may be needed
chmod-socket    = 666
# clear environment on exit
vacuum          = true

stats           = %(chdir)/config/uwsgi.status

pidfile         = %(chdir)/config/uwsgi.pid
EOF

#停止nginx 一切使用supervisor进行管理
systemctl stop nginx
killall nginx
# 禁止开机启动
systemctl disable nginx.service

# 创建supervisord 进程文件
cat <<EOF >> /etc/supervisord.d/${NAME}.conf
[program:$NAME] ; 程序名称，在 supervisorctl 中通过这个值来对程序进行一系列的操作
autorestart=True      ; 程序异常退出后自动重启
autostart=True        ; 在 supervisord 启动的时候也自动启动
environment=PATH="$ENV_PATH/bin"  ; 可以通过 environment 来添加需要的环境变量，一种常见的用法是使用指定的 virtualenv 环境
directory=$PRODUCT_DIR  ; 程序的启动目录
command=uwsgi --ini ${NAME}_uwsgi.ini  ; 启动命令，与手动在命令行启动的命令是一样的
user=root           ; 用哪个用户启动
EOF

cat <<EOF >> /etc/supervisord.d/service.conf
[program:nginx]
command=/usr/sbin/nginx -g 'daemon off;' -c /etc/nginx/nginx.conf
autostart=true
autorestart=true
user=root

EOF


# 设置supervisor开机启动
sed -i '/^exit 0/i\/bin/bash -c "/usr/local/bin/supervisord -c /etc/supervisord.conf"' /etc/rc.local
# 启动supervisord
chmod +x /etc/supervisord.conf
supervisord -c /etc/supervisord.conf
supervisorctl update
supervisorctl reload



# supervisord 基本操作命令
# supervisorctl reload
# supervisorctl status
# supervisorctl restart all
# supervisorctl restart xoj

# 启动命令在项目根目录下启动
# source $ENV_PATH/bin/activate
# cd $PRODUCT_DIR
# uwsgi --ini ${NAME}_uwsgi.ini

