# -*- coding: utf-8 -*-
from collections import OrderedDict
from rest_framework import exceptions

from rest_framework import mixins
from rest_framework import permissions, pagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.decorators import detail_route, list_route

from common_framework.utils import get_ip
from .serializers import BlogSerializers, TimeLineSerializers, BlogLikeSerializer
from .models import Blog, TimeLine, BlogLike


class BlogPagination(pagination.PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('pageNumber', self.page.paginator.num_pages),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('posts', data)
        ]))


class BlogViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all().order_by("-created_time")
    serializer_class = BlogSerializers
    permission_classes = (permissions.AllowAny,)
    pagination_class = BlogPagination

    def retrieve(self, request, *args, **kwargs):
        is_add_views = request.query_params.get('is_add_views')
        instance = self.get_object()
        if is_add_views == 'true':
            instance.increase_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @list_route()
    def get_hot(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(status='p')[:6]
        serializer_data = self.get_serializer(queryset, many=True,
                                              fields=('image', 'title', 'description')).data
        return Response(status=status.HTTP_200_OK, data=serializer_data)

    @detail_route(methods=['get'])
    def page_up_down(self, request, pk):
        pk = int(pk)
        ids_titles = list(self.get_queryset().values('id', 'title'))
        ids_titles.sort(key=lambda x: x['id'])

        current_blog_index = -1
        for index, id_title in enumerate(ids_titles):
            for key, v in id_title.items():
                if key == 'id' and v == pk:
                    current_blog_index = index

        if current_blog_index < 0:
            raise NotImplementedError('list_index 必须大于0')

        if current_blog_index == len(ids_titles)-1:
            next_blog_title = u'没有下一篇'
            next_blog = {
                'title': next_blog_title,
                'id': None
            }
            last_blog = ids_titles[current_blog_index - 1]
        elif current_blog_index == 0:
            last_blog_title = u'没有上一篇'
            last_blog = {
                'title': last_blog_title,
                'id': None
            }
            next_blog = ids_titles[current_blog_index + 1]
        else:
            next_blog = ids_titles[current_blog_index + 1]
            last_blog = ids_titles[current_blog_index - 1]

        data = {
            'next_blog': next_blog,
            'last_blog': last_blog
        }
        return Response(data=data, status=status.HTTP_200_OK)


class BlogLikeViewSet(CacheResponseMixin, mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    博客点赞
    """
    queryset = BlogLike.objects.all()
    serializer_class = BlogLikeSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        user = self.request.user
        anonymous_ip = get_ip(self.request)
        if self.get_queryset().filter(user_id=user.id, anonymous_ip=anonymous_ip, blog=serializer.validated_data['blog']).exists():
            raise exceptions.ValidationError("已经点过赞了")
        # 判断是否登录用户
        if user.is_authenticated:
            serializer.save(user=user, anonymous_ip=anonymous_ip)
        else:
            serializer.save(anonymous_ip=anonymous_ip)

    @list_route(methods=['get'])
    def get_blog_like_count(self, request):
        user = self.request.user
        anonymous_ip = get_ip(self.request)

        blog_id = request.query_params.get("blog_id")
        if not blog_id and not blog_id.isdigit():
            raise exceptions.ValidationError("参数错误")
        queryset = self.get_queryset()

        has_like = queryset.filter(user_id=user.id, anonymous_ip=anonymous_ip, blog_id=blog_id).exists()
        like_count = queryset.filter(blog_id=int(blog_id)).count()
        return Response(status=status.HTTP_200_OK, data={"count": like_count, "has_like": has_like})


class TimeLineViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = TimeLine.objects.all().order_by("-created_time")
    serializer_class = TimeLineSerializers
    permission_classes = (permissions.AllowAny, )
