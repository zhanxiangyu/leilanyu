# -*- coding: utf-8 -*-

import logging
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Blog, Category, Tag

User = get_user_model()

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    创建blog测试数据
    """

    help = 'create test data'

    def handle(self, *args, **options):
        user = User.objects.get_or_create(username='test用户', email='test@test.com', password='xctfoj01')[0]
        pcategory = Category.objects.get_or_create(name='我是父类目录', parent_category=None)[0]
        category = Category.objects.get_or_create(name='我是子目录', parent_category=pcategory)[0]

        category.save()
        basetag = Tag.objects.get_or_create(name='test标签')[0]
        basetag.save()

        for i in range(1, 20):
            blog = Blog.objects.get_or_create(title='blog_title' + str(i), body='blog_body' + str(i),
                                       author=user, category=category)[0]

            tag = Tag.objects.get_or_create(name='test标签' + str(i))[0]
            tag.save()
            blog.tags.add(tag)
            blog.tags.add(basetag)
            blog.save()
            print('create blog is the {}'.format(blog.title))
        pass
