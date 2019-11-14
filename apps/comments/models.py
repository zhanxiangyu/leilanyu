# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings

from blog.models import Blog


class BaseComment(models.Model):
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class Comment(BaseComment):
    body = models.TextField('评论内容', max_length=300)
    commentator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_user', verbose_name='评论人')
    article = models.ForeignKey(Blog, related_name='comment_blog', verbose_name='评论文章', null=True, blank=True)
    parent_comment = models.ForeignKey('self', related_name='sub_comment', blank=True, null=True, verbose_name='父级评论', on_delete=models.CASCADE)
    is_enable = models.BooleanField('是否显示', default=True)

    class Meta:
        ordering = ['created_time']
        verbose_name = '评论信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.body[:50]
