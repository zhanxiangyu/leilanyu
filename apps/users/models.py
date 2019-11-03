# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import user_logged_in

from .utils.utlis import get_client_ip_from_request
# from django.contrib.sites.models import Site


class User(AbstractUser):
    """
    用户信息表
    """
    MALE = 'male'
    FEMAlE = 'female'
    GENDER_CHOICES = (
        (MALE, u'男'),
        (FEMAlE, u'女'),
    )
    nick_name = models.CharField(verbose_name='用户昵称', max_length=100, blank=True, null=True)
    gender = models.CharField(verbose_name=u'性别', max_length=6, choices=GENDER_CHOICES, default=MALE)
    address = models.CharField(verbose_name=u'用户地址', max_length=100, default="", blank=True, null=True)
    moblie = models.CharField(verbose_name=u'手机号码', max_length=11, blank=True, null=True)
    image = models.ImageField(verbose_name=u'用户头像', upload_to='image/head/%Y/%m/%d', default='image/default.jpg')

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:about')

    def name(self):
        return self.nick_name and self.nick_name or self.username

    # def get_full_url(self):
    #     """
    #     获取当前网站域名，同时setting.py中INSTALLED_APPS需要添加'django.contrib.sites',
    #     """
    #     site = Site.objects.get_current().domain
    #     url = 'https://{site}{path}'.format(site=site, path=self.get_absolute_url())
    #     return url

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name


def get_last_login_ip(sender, user, request, **kwargs):
    """
    更新用户最后一次登陆的IP地址
    """
    ip = get_client_ip_from_request(request)
    if ip:
        if RecordIP.objects.filter(last_login_ip=ip, user=user).exists():
            record_id = RecordIP.objects.filter(last_login_ip=ip, user=user).first()
            record_id.user = user
            record_id.save()
        else:
            RecordIP.objects.create(
                last_login_ip=ip,
                user=user
            )


user_logged_in.connect(get_last_login_ip)


class EmailVerifyRecord(models.Model):
    """
    邮箱验证表
    """
    REGISTER = 'register'
    FORGET = 'forget'
    UPDATE = 'update'
    SEND_TYPE_CHOICES = (
        (REGISTER,u'注册'),
        (FORGET, u'找回密码'),
        (UPDATE, u'修改邮箱'),
    )
    code = models.CharField(verbose_name=u'验证码',max_length=20)
    email = models.EmailField(verbose_name=u'邮箱', max_length=50)
    send_type = models.CharField(verbose_name=u'验证类型', choices=SEND_TYPE_CHOICES, default=REGISTER, max_length=8)
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.email


class RecordIP(models.Model):
    """
    记录ip
    """
    user = models.ForeignKey(User, null=True, blank=True, related_name='to_recordip')
    last_login_ip = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.last_login_ip

    class Meta:
        verbose_name = u'登录ip记录'
        verbose_name_plural = verbose_name



