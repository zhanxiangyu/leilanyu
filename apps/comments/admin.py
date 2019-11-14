# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Comment


# actions添加模型动作
def disable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=False)


def enable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=True)


disable_commentstatus.short_description = '隐藏评论'
enable_commentstatus.short_description = '显示评论'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentator', "body", 'article', 'parent_comment', 'is_enable', 'created_time')
    list_display_links = ('id', 'commentator', "body")
    list_filter = ('commentator', 'article', 'is_enable')
    actions = [disable_commentstatus, enable_commentstatus]

    def formfield_for_foreignkey(self, db_field, request, *args, **kwargs):
        if db_field.name == 'parent_comment':
            try:
                obj_id = request.resolver_match.args[0]
                kwargs['queryset'] = Comment.objects.filter(parent_comment=None).exclude(id=int(obj_id))
            except:
                kwargs['queryset'] = Comment.objects.filter(parent_comment=None)
        return super(CommentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
