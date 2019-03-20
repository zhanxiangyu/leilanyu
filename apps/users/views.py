# -*- coding:utf-8 -*-
from datetime import datetime

from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.conf import settings
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response

from blog.models import Blog, Tag, FriendLink
from users.forms import RegisterForm
from .models import RecordIP
from .utils.utlis import get_client_ip_from_request

User = get_user_model()

# 配置全局返回
def template_variable(request):
    context = {}
    context['SITE_NAME'] = settings.SITE_NAME
    context['SITE_URL'] = settings.SITE_URL
    context['SITE_SEO_DESCRIPTION'] = settings.SITE_SEO_DESCRIPTION
    context['SITE_SEO_KEYWORDS'] = settings.SITE_SEO_KEYWORDS
    context['ADMIN_URL'] = settings.ADMIN_URL
    return context


@cache_page(60 * 5)
def index(request):
    queryset = Blog.objects.all()
    new_blogs = queryset.order_by('-pub_time')[:10]  # 最新发布

    click_sort_blogs = queryset.order_by('-views')[:6]  # 点击排行

    # 标签云
    tags = Tag.objects.all()[:10]
    friend_links = FriendLink.objects.all().order_by('-quanzhong')
    # 记录非登录用户
    if not request.user.is_authenticated():
        ip = get_client_ip_from_request(request)
        if ip:
            if not RecordIP.objects.filter(last_login_ip=ip).exists():
                RecordIP.objects.create(
                    last_login_ip=ip
                )
            else:
                record_ip = RecordIP.objects.filter(last_login_ip=ip).first()
                record_ip.last_mod_time = datetime.now
                record_ip.save()

    return render(request, 'index.html', locals())


def about_me(request):
    return render(request, 'about.html', locals())
    pass


def leave_message(request):
    return render(request, 'board.html', locals())


def login(request):
    next = request.GET.get('next', '/')  # 用于返回页面跳转
    return render(request, 'login.html', locals())


@login_required(login_url='index')
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('index'))


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def handler_login(request, authentication_form=AuthenticationForm):
    data = {}
    redirect_to = request.data.get('next', '/')
    form = authentication_form(request, data=request.data)
    if form.is_valid():
        # 重定向url
        user = form.get_user()
        django_login(request, user)
        data['redirect_url'] = _get_redirect_url(request, redirect_to)
    else:
        return Response(data={'errors': '用户名或密码不正确'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(data, status=status.HTTP_200_OK)


def _get_redirect_url(request, redirect_to):
    if not is_safe_url(redirect_to, host=request.get_host()):
        return resolve_url('users:login')
    return redirect_to


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'regist.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            # password2 = register_form.cleaned_data['password2']
            if User.objects.filter(username=username).exists():
                return render(request, 'regist.html', {'register_form': register_form, 'name_used': '用户名已经使用'})
            User.objects.create_user(
                username=username,
                password=password
            )
            return render(request, 'login.html', {'success': '注册成功'})
        return render(request, 'regist.html', {'register_form': register_form})
