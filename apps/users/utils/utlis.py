# -*- coding:utf-8 -*-
# __author__ = 'zhan'
# __date__ = '18-4-14 下午10:10'
import base64

from django.conf import settings
from django.core.mail import send_mail
from ipware import get_client_ip
from itsdangerous import URLSafeTimedSerializer as utsr
from common_framework.delay_task import new_task


def custom_send_mail(title, msg, from_email, to_email):
    if isinstance(to_email, (unicode, str)):
        to_email = [to_email]
    # if settings.DEBUG:
    #     send_mail(title, msg, from_email, to_email)
    # else:
    # 发送异常时不提示
    new_task(send_mail, 2, (title, msg, from_email, to_email))
    # send_mail(title, msg, from_email, to_email, fail_silently=True)


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


class Token():
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.salt = base64.encodestring(secret_key)

    def generate_validate_token(self, email):
        serializer = utsr(self.secret_key)
        return serializer.dumps(email, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.secret_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.secret_key)
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(settings.SECRET_KEY)



def get_active_msg(e, type):
    if 'age' in e.message and '>' in e.message:
        active_msg = '{type}链接已过期'.format(type=type)
    else:
        active_msg = '该链接异常, 请重新获取链接'
    return active_msg


