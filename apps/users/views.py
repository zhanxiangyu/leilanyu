# -*- coding:utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, resolve_url
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.decorators.cache import cache_page
from django.views.generic.base import View
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from blog.models import Blog, Tag, FriendLink
from users.forms import RegisterForm
from users.models import RecordIP
from users.utils.utlis import get_client_ip_from_request, token_confirm, get_active_msg
from users.utils.constants import expiration as time_expiration

User = get_user_model()


class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


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


def indexV(request):
    return render(request, 'index/index.html', locals())


def about_me(request):
    return render(request, 'about.html', locals())
    pass


def leave_message(request):
    return render(request, 'board.html', locals())


def login(request):
    next = request.GET.get('next', '/')  # 用于返回页面跳转
    # return render(request, 'login.html', locals())
    return render(request, 'user/logreg/login.html', locals())


@login_required
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
        response = JsonResponse(data=form.errors)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    return Response(data, status=status.HTTP_200_OK)


def _get_redirect_url(request, redirect_to):
    if not is_safe_url(redirect_to, host=request.get_host()):
        return resolve_url('users:login')
    return redirect_to


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user/logreg/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']

            # 默认用户未激活
            User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_active=False,
            )
            return JsonResponse(data={'redirect_url': resolve_url('users:login')})
        response = JsonResponse(data=register_form.errors)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


# 激活邮件，找回密码
def send_confirm_email(request, email_type):
    title = '激活账号'
    if email_type == 'pwd':
        title = '找回密码'
    return render(request, 'user/logreg/send_email.html', locals())


def forgetpwd(request, token):
    try:
        email = token_confirm.confirm_validate_token(token=token, expiration=time_expiration)
    except Exception as e:
        active_msg = get_active_msg(e, '找回密码')
    return render(request, 'user/logreg/forgetpwd.html', locals())


def active(request, token):
    active_msg = '激活成功'
    try:
        email = token_confirm.confirm_validate_token(token=token, expiration=time_expiration)
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                active_msg = '已激活'
                return render(request, 'user/logreg/login.html', locals())
            user.is_active = True
            user.save()
        except:
            active_msg = '激活用户不存在'
            return render(request, 'user/logreg/send_email.html', locals())
    except Exception as e:
        active_msg = get_active_msg(e, '激活')
        return render(request, 'user/logreg/send_email.html', locals())

    return render(request, 'user/logreg/login.html', locals())


# 个人中心
# 用户设置
@login_required
def user_settings(request):
    return render(request, 'user/settings.html', locals())

@login_required
def user_dynamic(request):
    return render(request, 'user/dynamic.html', locals())

# 配置404， 403， 500页面
def permission_denied(request):
    return render(request, 'error/403.html', locals())


def page_not_found(request):
    return render(request, 'error/404.html', locals())


def page_error(request):
    return render(request, 'error/500.html', locals())
