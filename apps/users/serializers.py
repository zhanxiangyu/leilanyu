# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import RecordIP

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = "__all__"
    pass


class RecordIPSerializers(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    # user_image_url = serializers.URLField(source='user.image.url')

    def get_user_image(self, obj):
        if obj.user:
            return obj.user.image.url
        return None

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return None

    class Meta:
        model = RecordIP
        fields = "__all__"
