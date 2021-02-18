from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from appAPI.models import *
from appAPI.serializers import *

# Create your views here.


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        try:
            userId = Userex.objects.get(email=email)
            serializer = UserexSerializer(userId)
            if email == serializer.data['email']:
                if password == serializer.data['password']:
                    return Response('เข้าสู้ระบบ',status=status.HTTP_202_ACCEPTED)
                else:
                    return Response('รหัสผ่านไม่ถูก', status=status.HTTP_200_OK)
        except Userex.DoesNotExist:
            return Response('อีเมลไม่ถูกต้อง', status=status.HTTP_200_OK)
        

@api_view(['POST'])
def user_api(request):
    if request.method == 'POST':
        serializer = UserexSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api(request, pk):
    """
    Retrieve, update or delete a user.
    """
    try:
        userId = Userex.objects.get(pk=pk)
    except Userex.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserexSerializer(userId)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserexSerializer(userId, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        userId.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
