# -*- coding: utf-8 -*-
import hmac
from hashlib import sha1
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.encoding import force_bytes

import requests
from ipaddress import ip_address, ip_network

# {'HISTTIMEFORMAT': 'root %Y/%m/%d %T ', 'wsgi.multiprocess': False, 'RUN_MAIN': 'true', 'HTTP_X_HUB_SIGNATURE': 'sha1=73471b158c6ff5e2c0059012782fc0e216318ff3', 'SERVER_PROTOCOL': 'HTTP/1.1', 'LC_TERMINAL_VERSION': '3.3.4', 'SCRIPT_NAME': u'', 'LESSOPEN': '| /usr/bin/lesspipe %s', 'SSH_CLIENT': '221.226.9.54 56539 22', 'REQUEST_METHOD': 'POST', 'LOGNAME': 'root', 'USER': 'root', 'PROMPT_COMMAND': 'history -a;', 'PATH': '/root/.virtualenvs/leilanyu/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin', 'QUERY_STRING': '', 'HOME': '/root', 'PS1': '(leilanyu) \\[\\e]0;\\u@\\h: \\w\\a\\]${debian_chroot:+($debian_chroot)}\\u@\\h:\\w\\$ ', 'LANG': 'en_US.UTF-8', 'LC_TERMINAL': 'iTerm2', 'TERM': 'xterm-new', 'SHELL': '/bin/bash', 'TZ': 'Asia/Shanghai', 'SERVER_NAME': 'instance-htlbwv74.novalocal', 'REMOTE_ADDR': '192.30.252.90', 'SHLVL': '1', 'HISTSIZE': '1000', 'wsgi.url_scheme': 'http', 'SERVER_PORT': '80', 'CONTENT_LENGTH': '9204', 'HISTFILESIZE': '10000', 'WORKON_HOME': '/root/.virtualenvs', 'XDG_RUNTIME_DIR': '/run/user/0', 'wsgi.file_wrapper': <class wsgiref.util.FileWrapper at 0x7f522a339db8>, 'SERVER_SOFTWARE': 'WSGIServer/0.1 Python/2.7.12', 'VIRTUAL_ENV': '/root/.virtualenvs/leilanyu', 'HTTP_X_GITHUB_DELIVERY': '4df2d180-fabe-11e9-8b3e-68f468d298ad', 'wsgi.input': <socket._fileobject object at 0x7f521f3efe50>, 'VIRTUALENVWRAPPER_WORKON_CD': '1', 'HTTP_HOST': '106.12.72.157', 'wsgi.multithread': True, 'wsgi.version': (1, 0), 'XDG_SESSION_ID': '168', '_': '/root/.virtualenvs/leilanyu/bin/python', 'HTTP_ACCEPT': '*/*', 'VIRTUALENVWRAPPER_PROJECT_FILENAME': '.project', 'SSH_CONNECTION': '221.226.9.54 56539 192.168.0.4 22', 'LESSCLOSE': '/usr/bin/lesspipe %s %s', 'VIRTUALENVWRAPPER_HOOK_DIR': '/root/.virtualenvs', 'GATEWAY_INTERFACE': 'CGI/1.1', 'wsgi.run_once': False, 'SSH_TTY': '/dev/pts/0', 'OLDPWD': '/home', 'HTTP_X_GITHUB_EVENT': 'ping', 'HTTP_USER_AGENT': 'GitHub-Hookshot/886c9d1', 'VIRTUALENVWRAPPER_SCRIPT': '/usr/local/bin/virtualenvwrapper.sh', 'PWD': '/home/leilanyu', 'DJANGO_SETTINGS_MODULE': 'leilanyu.settings', 'CONTENT_TYPE': 'application/x-www-form-urlencoded', 'MAIL': '/var/mail/root', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:', 'REMOTE_HOST': '', 'wsgi.errors': <open file '<stderr>', mode 'w' at 0x7f523113c1e0>, 'PATH_INFO': u'/webhook/'}

@require_POST
@csrf_exempt
def webhook(request):
    # import pdb
    # pdb.set_trace()
    # forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    # client_ip_address = ip_address(forwarded_for)  # 获取发送请求的ip--客户端ip
    client_ip_address = request.META.get('REMOTE_ADDR')  # 获取发送请求的ip--客户端ip
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    # 获取github hooks的白名单
    for valid_ip in whitelist:
        ips = [ip_network_valid_ip.exploded for ip_network_valid_ip in ip_network(valid_ip)]
        if client_ip_address in ips:
            break
    else:
        return HttpResponseForbidden('Permission denied. ip not allow ')

    # Verify the request signature
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied signature.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return HttpResponseServerError('Operation not supported.', status=501)

    mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden('Permission denied. signature not match')

    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        return HttpResponse('success')

    # In case we receive an event that's not ping or push
    return HttpResponse(status=204)
    # os.system('cd /var/www/admin')
    # os.system('git pull -f git@github.com:haoflynet/admin.git 2>&1')
