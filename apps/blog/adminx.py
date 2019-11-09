# -*- coding: utf-8 -*-
import xadmin
from blog.models import Blog, TimeLine, Tag, Category, FriendLink


class BlogAdmin(object):
    list_display = ('title', 'created_time', 'status', 'comment_status', 'author')
    model_icon = 'fa fa-file-text'


class TimeLineAdmin(object):
    list_display = ('title', 'text', 'created_time',)
    model_icon = 'fa fa-arrows-v'


class TagAdmin(object):
    list_display = ('name', 'created_time',)
    model_icon = 'fa fa-tags'


class CategoryAdmin(object):
    list_display = ('name', 'parent_category', 'created_time')
    model_icon = "fa fa-tasks"


class FriendlinkAdmin(object):
    list_display = ('name', 'url', 'last_mod_time')
    model_icon = "fa fa-tasks"


xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(TimeLine, TimeLineAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(FriendLink, FriendlinkAdmin)
