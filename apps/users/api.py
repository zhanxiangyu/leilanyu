# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import RecordIP
from .serializers import RecordIPSerializers


class RecordIPViewSet(CacheResponseMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = RecordIP.objects.all().order_by('-last_mod_time')[:8]
    serializer_class = RecordIPSerializers
    permission_classes = (permissions.AllowAny,)

