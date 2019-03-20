# coding:utf-8
from django.contrib import admin

from models import Blog, Category, Tag, FriendLink, TimeLine


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'type', 'views', 'author', 'category', 'last_mod_time')
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'last_mod_time',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_mod_time')


class FriendlinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'quanzhong', 'created_user')
    readonly_fields = ('created_user',)

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.created_user = user
        obj.save()


class TimeLineAdmin(admin.ModelAdmin):
    list_display = ("title", "created_time", "last_mod_time")


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(FriendLink, FriendlinkAdmin)
admin.site.register(TimeLine, TimeLineAdmin)
