# -*- coding: utf-8 -*-
import logging
from django.core.cache import cache

from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializers, CommentCreateSerializers

logger = logging.getLogger(__name__)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        queryset = self.queryset.all()
        # queryset = Comment.objects.filter(parent_comment=None)
        blog_id = self.request.query_params.get('blog_id', None)
        if blog_id is not None:
            queryset = queryset.filter(article_id=blog_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        重写创建帖子方法，使用PostDetailSerializer
        """
        serializer = CommentCreateSerializers(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        serializer.save(commentator=self.request.user)
        cache.clear()

    # def extra_handle_list_data(self, data):
    #     comment_dict = {}
    #     comment_child = {}
    #     comment_request ={}
    #     for comment in data:
    #         if comment['parent_comment'] != None:
    #             parent_id = comment['parent_comment']
    #             comment_child.setdefault(parent_id, []).append(comment)
    #         else:
    #             parent_id = comment['id']
    #             comment_dict.setdefault(parent_id, []).append(comment)
    #     for k, v in comment_dict.items():
    #         comment_request.setdefault(k, []).append(v)
    #     for k, v in comment_child.items():
    #         comment_request.setdefault(k, []).append(v)
    #     logger.info('handle_list_data is over!!!')
    #     logger.error('handle_list_data errors...')
    #     logger.debug('handle_list_data debug..')
    #     logger.warning('handle_list_dat warning..')
    #     return comment_request
