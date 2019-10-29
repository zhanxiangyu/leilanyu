# -*- coding:utf-8 -*-
"""leilanyu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from common_framework.webhook import webhook

from users.views import index, indexV
from blog.search_views import MySearchView

import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()


urlpatterns = [
    url(r'^'+settings.ADMIN_URL+'/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^captcha/', include('captcha.urls')),
    # url(r'^auth/', include('rest_framework_social_oauth2.urls')),

    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^comments/', include('comments.urls', namespace='comments')),

    url(r'^$', indexV, name='index'),
    url(r'^v1$', index, name='home'),

    url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^docs/', include_docs_urls(title=u'累兰羽 api 文档')),


    url(r'^search/', MySearchView(), name="haystack_search"),

    # 项目自动更新
    url(r'^webhook/$', webhook, name='webhook'),
]

handler403 = 'users.views.permission_denied'
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
