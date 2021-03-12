from django.db.models import fields
from django.db.models.base import Model
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

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = 'report_id', 'message', 'reporter', 'report_to', 'pet_id'

class UserReportSerializer(serializers.ModelSerializer):    
    reporter = ReportSerializer(many=True, read_only=True)  
    class Meta:
        model = Userex
        fields = 'user_id', 'first_name', 'last_name', 'user_image', 'reporter'

class PetImagesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = 'pet_id', 'pet_image'

class PetReportSerializer(serializers.ModelSerializer):
    petImages = PetImagesReportSerializer(many=True, read_only=True)
    class Meta:
        model = Pet
        fields = 'animal_type', 'species', 'birth_year', 'sex', 'disease', 'petImages'


        
