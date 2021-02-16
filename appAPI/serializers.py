from django.db.models import fields
from appAPI.models import Userex
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
        models = Userex
        fields = '__all__'
