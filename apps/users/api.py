# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from users.models import RecordIP, User
from users.serializers import RecordIPSerializers, UserSerializers


class RecordIPViewSet(CacheResponseMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = RecordIP.objects.all().order_by('-last_mod_time')[:8]
    serializer_class = RecordIPSerializers
    permission_classes = (permissions.AllowAny,)



class UserViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


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
