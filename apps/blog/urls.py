# -*- coding:utf-8 -*-
# __author__ = 'zhan'
# __date__ = '17-12-31 下午2:01'
from django.conf.urls import url, include
from rest_framework import routers

from . import views
from .api import BlogViewSet, TimeLineViewSet, BlogLikeViewSet

router = routers.DefaultRouter()
router.register("blog", BlogViewSet)
router.register("timeline", TimeLineViewSet)
router.register("like", BlogLikeViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^detail/(?P<blog_id>\d+)/$', views.blog_detail, name='blog_detail'),
    url(r'^tag/(?P<tag_id>[0-9a-z]+)/$', views.blog_tag, name='blog_tag'),
    url(r'^category/(?P<category_id>[0-9a-z]+)/$', views.blog_category, name='blog_category'),
    url(r'^mood/$', views.blog_mood, name='blog_mood'),
    url(r'^list/$', views.list, name='blog_list'),
]
