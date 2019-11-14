# coding:utf-8
from django.contrib import admin

from models import Blog, Category, Tag, FriendLink, TimeLine, BlogLike


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'type', 'views', 'author', 'category', 'last_mod_time')
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'last_mod_time',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_mod_time')


@admin.register(FriendLink)
class FriendlinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'quanzhong', 'created_user')
    readonly_fields = ('created_user',)

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.created_user = user
        super(FriendlinkAdmin, self).save_model(request, obj, form, change)


@admin.register(TimeLine)
class TimeLineAdmin(admin.ModelAdmin):
    list_display = ("title", "created_time", "last_mod_time")


@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "anonymous_ip", "created_time")