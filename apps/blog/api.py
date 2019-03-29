# -*- coding: utf-8 -*-
from collections import OrderedDict

from rest_framework import mixins
from rest_framework import permissions, pagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.decorators import detail_route, list_route

from .serializers import BlogSerializers, TimeLineSerializers
from .models import Blog, TimeLine


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
        pass


class TimeLineViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = TimeLine.objects.all().order_by("-created_time")
    serializer_class = TimeLineSerializers
    permission_classes = (permissions.AllowAny, )
