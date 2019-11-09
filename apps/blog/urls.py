# -*- coding:utf-8 -*-
# __author__ = 'zhan'
# __date__ = '17-12-31 下午2:01'
from django.conf.urls import url, include
from rest_framework import routers

from . import views
from .api import BlogViewSet, TimeLineViewSet, BlogLikeViewSet, get_tags_and_friends

router = routers.DefaultRouter()
router.register("blog", BlogViewSet)
router.register("timeline", TimeLineViewSet)
router.register("like", BlogLikeViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/get_tags_and_friends/$', get_tags_and_friends, name='get_tags_and_friends'),
    url(r'^detail/(?P<blog_id>\d+)/$', views.blog_detail, name='blog_detail'),
    url(r'^list/$', views.list, name='blog_list'),
]
