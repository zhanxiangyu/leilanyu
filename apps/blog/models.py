# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import markdown

from django.db import models
from django.conf import settings

from django.urls import reverse


class BlogManager(models.Manager):

    def get_queryset(self, ):
        return super(BlogManager, self).get_queryset().filter(status='p').order_by("-created_time")


class Blog(models.Model):
    """
    博客文章表
    """
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    pub_time = models.DateTimeField('发布时间', blank=True, null=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='d')
    comment_status = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('浏览量', default=0)
    image = models.ImageField(verbose_name=u'文章头像', upload_to='image/blog', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    description = models.CharField("文章描述", max_length=30, default='')

    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    objects = models.Manager()
    public = BlogManager()

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={'blog_id': self.pk})

    class Meta:
        ordering = ['-pub_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        # get_latest_by = 'created_time'

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class BlogLike(models.Model):
    """
    用户点赞
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建者', null=True, blank=True,
                             related_name="to_like")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    anonymous_ip = models.CharField(verbose_name="匿名用户ip", max_length=20, null=True, blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = "点赞统计"
        verbose_name_plural = verbose_name


class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名', max_length=30, unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    # def get_absolute_url(self):
    #     return reverse('blog:category_detail', kwargs={'category_name': self.pk})

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名', max_length=10, unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('blog:tag_detail', kwargs={'tag_name': self.slug})


    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class FriendLink(models.Model):
    """
    友情链接, 隔壁邻居
    """
    name = models.CharField('链接名称', max_length=50, unique=True)
    url = models.URLField('链接')
    quanzhong = models.PositiveIntegerField('权重', default=10, help_text="权重越高，显示越靠前")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建者',on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name


class TimeLine(models.Model):
    """
    时间线
    """
    title = models.CharField('标题', max_length=35)
    text = models.TextField('主体')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '时间线'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

    pass