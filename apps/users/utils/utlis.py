# -*- coding:utf-8 -*-
# __author__ = 'zhan'
# __date__ = '18-4-14 下午10:10'

from django.conf import settings
from ipware import get_client_ip


def get_client_ip_from_request(request):
    """
    返回request里的IP地址
    提示：
        为了开发方便，这个函数会返回类似127.0.0.1之类无法在公网被路由的地址，
        在生产环境中，类似地址不会被返回
    """
    client_ip, is_routable = get_client_ip(request)
    if settings.DEBUG:
        return client_ip
    else:
        if client_ip is not None and is_routable:
            return client_ip
    return None
    pass