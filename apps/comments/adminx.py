# -*- coding: utf-8 -*-
import xadmin
from comments.models import Comment


class CommentAdmin(object):
    list_display = ('body', 'commentator', 'article', 'parent_comment', 'is_enable')
    model_icon = 'fa fa-at'


xadmin.site.register(Comment, CommentAdmin)
