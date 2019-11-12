# -*- coding: utf-8 -*-
from collections import OrderedDict
from rest_framework import exceptions

from rest_framework import mixins
from rest_framework import permissions, pagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.decorators import action, api_view, permission_classes

from common_framework.utils import get_ip
from .serializers import BlogSerializers, TimeLineSerializers, BlogLikeSerializer, TagSerializers, FriendLinkSerializers
from .models import Blog, TimeLine, BlogLike, Tag, FriendLink


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

    def get_queryset(self):
        queryset = super(BlogViewSet, self).get_queryset()
        tag_id = self.request.query_params.get('tag_id')
        if tag_id and tag_id.isdigit():
            queryset = queryset.filter(tags=int(tag_id))
        return queryset

    @action(methods=['get'], detail=False)
    def get_hot(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(status='p')[:6]
        serializer_data = self.get_serializer(queryset, many=True,
                                              fields=('image', 'title', 'description')).data
        return Response(status=status.HTTP_200_OK, data=serializer_data)

    @action(methods=['get'], detail=True)
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

        if current_blog_index == len(ids_titles) - 1:
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
        if self.get_queryset().filter(user_id=user.id, anonymous_ip=anonymous_ip,
                                      blog=serializer.validated_data['blog']).exists():
            raise exceptions.ValidationError("已经点过赞了")
        # 判断是否登录用户
        if user.is_authenticated:
            serializer.save(user=user, anonymous_ip=anonymous_ip)
        else:
            serializer.save(anonymous_ip=anonymous_ip)

    @action(methods=['get'], detail=False)
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
    permission_classes = (permissions.AllowAny,)


class TagViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = (permissions.AllowAny,)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_tags_and_friends(request):
    """
    获取友情链接和标签列表
    :param request:
    :return:
    """
    tags = Tag.objects.all()
    friendlink = FriendLink.objects.all()
    tags_data = TagSerializers(tags, many=True, fields=('id', 'name')).data
    friendlink_data = FriendLinkSerializers(friendlink, many=True, fields=('name', 'url')).data
    return Response(status=status.HTTP_200_OK, data={"tags": tags_data, "links": friendlink_data})
