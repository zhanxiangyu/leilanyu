# -*- coding: utf-8 -*-
from django.utils.crypto import get_random_string

def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.META:
        return request.META['REMOTE_ADDR']
    else:
        return None


def generate_git_webhook_key():
    return get_random_string(50)
