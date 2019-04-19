# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import RecordIP
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = "__all__"
    pass

class UserPatchSerializers(serializers.ModelSerializer):

    def to_internal_value(self, data):
        password = data.get('password', None)
        if password is not None:
            data._mutable = True
            if password == '':
                del data['password']
            else:
                data['password'] = make_password(password)
            data._mutable = False

        return super(UserPatchSerializers, self).to_internal_value(data)

    class Meta:
        model = User
        fields = "__all__"


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
