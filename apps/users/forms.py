# -*- coding: utf-8 -*-

from captcha.fields import CaptchaField
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=4)
    password = forms.CharField(required=True, max_length=8, min_length=3)
    password2 = forms.CharField(required=True, max_length=8, min_length=3)
    # 验证码,参数：错误信息
    captcha = CaptchaField(error_messages={'invalid': '验证码错误啊', "required": '验证码必填'})


    # 验证单个字段
    def clean_username(self):
        data = self.cleaned_data['username']
        if "admin" in data:
            raise forms.ValidationError("用户名不允许存在admin字符")
        return data

    # 验证字段
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('两次密码不一致')
        return self.cleaned_data
