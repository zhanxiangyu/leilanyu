# -*- coding:utf-8 -*-
import markdown
from django.shortcuts import render, get_object_or_404

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.
from blog.models import Blog, Tag, Category

def blog_detail(request, blog_id):
    """
    博客详情页
    """
    return render(request, 'blog/detail.html', locals())


def list(request):
    """
    博客列表页
    :param request:
    :return:
    """
    return render(request, 'blog/list.html', locals())
