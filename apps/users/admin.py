# coding:utf-8
from django.contrib import admin
from models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick_name', 'username', 'email', 'gender', 'is_active', 'date_joined', 'last_login')
    list_display_links = ('id', 'username')

# admin.site.register(User, UserAdmin)
