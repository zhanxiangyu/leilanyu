# -*- coding: utf-8 -*-

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=2)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=8, min_length=3)
    password2 = forms.CharField(required=True, max_length=8, min_length=3)
    # 验证码,参数：错误信息
    # captcha = CaptchaField(error_messages={'invalid': '验证码错误啊', "required": '验证码必填'})


    # 验证单个字段
    def clean_username(self):
        data = self.cleaned_data['username']
        if "admin" in data:
            raise forms.ValidationError("用户名不允许存在admin字符")
        if "@" in data:
            raise forms.ValidationError("用户名不允许存在@字符")
        return data

    # 验证字段
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('两次密码不一致')
        username = self.cleaned_data['username']
        email = self.cleaned_data['username']
        user = User.object.filter(Q(username=username) | Q(email=email))
        if user.exists():
            raise forms.ValidationError("用户名或邮箱已存在")
        return self.cleaned_data
