# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from users.models import RecordIP, User
from users.serializers import RecordIPSerializers, UserSerializers
from users.utils.utlis import token_confirm, custom_send_mail


class RecordIPViewSet(CacheResponseMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = RecordIP.objects.all().order_by('-last_mod_time')[:8]
    serializer_class = RecordIPSerializers
    permission_classes = (permissions.AllowAny,)



class UserViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (permissions.AllowAny,)


    @list_route(methods=['POST'])
    def check_user_register(self, request):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        if username:
            queryset = self.queryset.filter(username=username)
            if queryset.exists():
                return Response(data=False, status=HTTP_200_OK)
        if email:
            queryset = self.queryset.filter(email=email)
            if queryset.exists():
                return Response(data=False, status=HTTP_200_OK)
        return Response(data=True, status=HTTP_200_OK)

    @list_route(methods=['POST',])
    def send_active_eamil(self, request):
        email = request.data.get('email', '')
        if not email:
            raise ValidationError('邮箱不能为空')

        # url = self.request.build_absolute_uri()
        http_host = request.META['HTTP_ORIGIN']
        token_code = token_confirm.generate_validate_token(email)

        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = email
        title = '累兰羽网站邀请你激活'
        msg = '点击激活链接进行用户激活：{http_host}{path}'.format(http_host=http_host,
                                                       path=reverse('users:active_user', kwargs={'token': token_code}))

        custom_send_mail(title, msg, email_from, email_to)
        return Response(data=True, status=HTTP_200_OK)