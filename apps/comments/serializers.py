# -*- coding: utf-8 -*-
from rest_framework import serializers

from blog.models import Blog
from users.models import User
from .models import Comment
from common_framework.handleserializers import ChangeSerializerFields


class CommentUserSerializer(ChangeSerializerFields, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.name()

    class Meta:
        model = User
        fields = '__all__'


class CommentBlogSerializer(ChangeSerializerFields, serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class CommentChildernSerializer(ChangeSerializerFields, serializers.ModelSerializer):
    commentator = CommentUserSerializer(fields=('id', 'username', 'email', 'image'))
    created_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return obj.created_time.strftime("%Y-%m-%d %H:%I:%S")

    class Meta:
        model = Comment
        fields = '__all__'

#  这种方式比较消耗服务器性能
# class CommentSerializers(serializers.ModelSerializer):
#     commentator = CommentUserSerializer(fields=('id', 'username', 'email', 'image'))
#     # article = CommentBlogSerializer(fields=('id', 'title', 'status'))
#     # parent_comment = CommentChildernSerializer(fields=('id', 'body', 'is_enable', 'commentator'))
#     sub_comment = CommentChildernSerializer(fields=('id', 'body', 'is_enable', 'commentator', 'created_time'),
#                                             many=True)
#     created_time = serializers.SerializerMethodField()
#
#     def get_created_time(self, obj):
#         return obj.created_time.strftime("%Y-%m-%d %H:%I:%S")
#
#     class Meta:
#         model = Comment
#         fields = '__all__'


# 返回数据给前台递归
class CommentSerializers(serializers.ModelSerializer):
    commentator = CommentUserSerializer(fields=('id','email', 'image', 'name'))
    created_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return obj.created_time.strftime("%Y-%m-%d %H:%I:%S")

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("parent_comment", "body", "article", "is_enable")

