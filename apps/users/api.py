# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.urls import reverse
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from users.models import RecordIP, User
from users.serializers import RecordIPSerializers, UserSerializers, UserPatchSerializers
from users.utils.constants import expiration as time_expiration
from users.utils.utlis import token_confirm, custom_send_mail, get_active_msg


class RecordIPViewSet(CacheResponseMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = RecordIP.objects.all().order_by('-last_mod_time')[:8]
    serializer_class = RecordIPSerializers
    permission_classes = (permissions.AllowAny,)



class UserViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UserPatchSerializers
        return self.serializer_class

    def perform_update(self, serializer):
        old_image_name = serializer.instance.image.name
        old_image_path = serializer.instance.image.path

        new_instance = serializer.save()

        if old_image_name != new_instance.image.name and os.path.exists(old_image_path):
            os.remove(old_image_path)


    @list_route(methods=['POST'], permission_classes=(permissions.AllowAny,))
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

    @list_route(methods=['POST',], permission_classes=(permissions.AllowAny,))
    def send_eamil(self, request):
        email = request.data.get('email', '')
        if not email:
            raise ValidationError('邮箱不能为空')
        email_type = request.data.get('email_type', '')

        # url = self.request.build_absolute_uri()
        http_host = request.META['HTTP_ORIGIN']
        token_code = token_confirm.generate_validate_token(email)

        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = email
        title = '累兰羽网站邀请你激活'
        msg = '点击激活链接进行用户激活：{http_host}{path}'.format(http_host=http_host,
                                                       path=reverse('users:active_user', kwargs={'token': token_code}))
        if email_type == 'pwd':
            title = '累兰羽网站找回密码'
            msg = '点击找回密码链接进行密码重置： {http_host}{path}'.format(http_host=http_host,
                                                             path=reverse('users:forget_pwd', kwargs={'token': token_code}))

        custom_send_mail(title, msg, email_from, email_to)
        return Response(data=True, status=HTTP_200_OK)

    @list_route(methods=['POST', ])
    def reset_pwd(self, request):
        pwd = request.data.get('password', '')
        pwd2 = request.data.get('password2', '')

        if not pwd or not pwd == pwd2:
            raise ValidationError('两次密码不一致')
        if len(pwd) < 5 or len(pwd) > 30:
            raise ValidationError('密码不规范')

        token = request.data.get('token', '')
        try:
            email = token_confirm.confirm_validate_token(token=token, expiration=time_expiration)
        except Exception as e:
            active_msg = get_active_msg(e, '找回密码')
            return Response(data=active_msg, status=HTTP_400_BAD_REQUEST)

        user=User.objects.filter(email=email).first()
        if not user:
            raise ValidationError('该用户不存在')

        user.set_password(pwd)
        user.save()
        return Response(data={'redirect_url': reverse('users:login')}, status=HTTP_200_OK)