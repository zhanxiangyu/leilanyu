# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers

from .api import CommentViewSet

router = routers.DefaultRouter()
router.register(r'comment', CommentViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
]
