# coding:utf-8
from django.contrib import admin
from models import User


# class MyAdminSite(admin.AdminSite):
#     site_header = '个人博客管理系统'
#     site_title = '累兰羽博客系统'


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick_name', 'username', 'email', 'gender', 'is_active', 'date_joined', 'last_login')
    list_display_links = ('id', 'username')


admin.AdminSite.site_header = '个人博客管理系统'
admin.AdminSite.site_title = '累兰羽博客系统'
admin.site.register(User, UserAdmin)