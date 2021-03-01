from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from appAPI.models import *
from appAPI.serializers import *
import json

# Create your views here.

# User
@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        try:
            userId = Userex.objects.get(email=email)
            serializer = UserexSerializer(userId)
            if email == serializer.data['email']:
                if password == serializer.data['password']:
                    return Response({'message': 'เข้าสู่ระบบสำเร็จ', 'email': email}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'message': 'รหัสผ่านไม่ถูก'}, status=status.HTTP_200_OK)
        except Userex.DoesNotExist:
            return Response({'message': 'อีเมลไม่ถูกต้อง'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_check_type_api(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        try:
            userId = Userex.objects.get(email=token)
            serializer = UserexSerializer(userId)
            return Response({'user_type': serializer.data['user_type']}, status=status.HTTP_202_ACCEPTED)
        except Userex.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def user_check_id_api(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        try:
            userId = Userex.objects.get(email=token)
            serializer = UserexSerializer(userId)
            return Response({'user_type': serializer.data['user_type']}, status=status.HTTP_202_ACCEPTED)
        except Userex.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def user_create_api(request):
    if request.method == 'POST':
        serializer = UserexSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PATCH', 'DELETE'])
def user_detail_api(request):
    """
    Retrieve, update or delete a user.
    """
    try:
        token = request.headers.get('Authorization')
        userId = Userex.objects.get(email=token)
    except Userex.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        newDict = UserexSerializer(userId).data
        newDict.pop('password')
        return Response(newDict)

    elif request.method == 'PATCH':
        serializer = UserexSerializer(userId, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        userId.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Pets
@api_view(['POST'])
def pet_create_api(request):
    request.data._mutable = True
    if request.method == 'POST':
        try:
            token = request.headers.get('Authorization')
            userId = Userex.objects.get(email=token)
            serializerUserex = UserexSerializer(userId)
            request.data.update({'owner_id': serializerUserex.data['user_id']})
        except Userex.DoesNotExist:
            return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        serializer = PetSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Pets images
@api_view(['POST'])
def pet_image_api(request):
    if request.method == 'POST':
        try:
            token = request.headers.get('Authorization')
            userId = Userex.objects.get(email=token)
        except Userex.DoesNotExist:
            return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        serializer = PetImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_201_CREATED)
