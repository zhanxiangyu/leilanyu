# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import serializers
from common_framework.handleserializers import ChangeSerializerFields

from .models import Blog, TimeLine


class BlogSerializers(ChangeSerializerFields, serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    category_name_url = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_category_name_url(self, obj):
        if obj.category:
            return reverse("blog:blog_category", kwargs={"category_id": obj.category.id})
        return '#'

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return ''

    def get_detail_url(self, obj):
        return reverse("blog:blog_detail", kwargs={'blog_id': obj.id})

    def get_username(self, obj):
        return obj.author.username

    def get_description(self, obj):
        if obj.description == '':
            return '暂无描述'
        return obj.description

    class Meta:
        model = Blog
        fields = "__all__"


class TimeLineSerializers(serializers.ModelSerializer):
    class Meta:
        model = TimeLine
        fields = "__all__"
