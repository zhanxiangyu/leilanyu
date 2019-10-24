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
    # blog_id = int(blog_id)
    # blog = get_object_or_404(Blog, pk=blog_id)
    # blog.views += 1
    # blog.save()
    #
    # md = markdown.Markdown(extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     # 'markdown.extensions.toc',
    #     TocExtension(slugify=slugify),
    # ])
    # blog.body = md.convert(blog.body)
    # toc = md.toc

    # blog.body = markdown.markdown(blog.body, extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc',
    # ])

    # try:
    #     last_blog = Blog.objects.filter(id__gt=blog_id)[0]
    #     last_blog_title = last_blog.title
    #     last_blog_id = last_blog.id
    # except:
    #     last_blog_title = '没有上一篇'
    #     last_blog_id = None
    #
    # try:
    #     next_blog = Blog.objects.filter(id__lt=blog_id)[0]
    #     next_blog_title = next_blog.title
    #     next_blog_id = next_blog.id
    # except:
    #     next_blog_title = '没有下一篇'
    #     next_blog_id = None
    return render(request, 'blog/detail.html', locals())


def blog_category(request, category_id):
    """
    学无止境:分类
    """
    content = {}
    category_id = int(category_id)
    blogs = Blog.objects.filter(category_id=category_id)
    try:
        cate = Category.objects.get(pk=category_id)
        content['cate_name'] = cate.name
    except:
        content['cate_name'] = '所有分类'

    return render(request, 'article.html', locals())

    pass


def blog_tag(request, tag_id='all'):
    """
    学无止境: 标签
    """
    if tag_id != 'all':
        tag_id = int(tag_id)
        tag = get_object_or_404(Tag, pk=tag_id)
        blogs = tag.blog_set.all()
        tag_name = tag.name
    else:
        blogs = Blog.objects.all()
        tag_name = '所有标签'
    return render(request, 'article.html', locals())


def blog_mood(request):
    """
    碎言碎语 , 时间线
    """
    blogs = Blog.objects.all().order_by('-created_time')
    return render(request, 'mood.html', locals())


def list(request):
    return render(request, 'blog/list.html', locals())
