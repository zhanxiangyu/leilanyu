# -*- coding:utf-8 -*-
# __author__ = 'zhan'
# __date__ = '17-12-31 下午2:00'
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from users import views
from users.api import RecordIPViewSet

router = DefaultRouter()
router.register('recordip', RecordIPViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^about/$', views.about_me, name='about_me'),
    url(r'^leave_message/$', views.leave_message, name='leave_message'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^handler_login/$', views.handler_login, name='handler_login'),
]
