from django.db.models import fields
from appAPI.models import *
from django.contrib.auth.models import User, Group
from django.db import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userex
        fields = '__all__'

        def user_image_url(self, Userex):
            request = self.context.get('request')
            image_url = Userex.user_image.url
            return request.build_absolute_uri(image_url)


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'


class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = '__all__'

        def pet_image_url(self, Userex):
            request = self.context.get('request')
            image_url = PetImage.pet_image.url
            return request.build_absolute_uri(image_url)


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
