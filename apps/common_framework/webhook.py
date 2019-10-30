# -*- coding: utf-8 -*-
import hmac
from hashlib import sha1
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.encoding import force_bytes

import requests
from ipaddress import ip_network


# @require_POST
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
