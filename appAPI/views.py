from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from appAPI.serializers import *
from rest_framework import viewsets


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
                    if serializer.data['status'] == 'on':
                        return Response({'message': 'เข้าสู่ระบบสำเร็จ', 'email': email},
                                        status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response({'message': 'บัญชีถูกระงับ', 'email': ''}, status=status.HTTP_200_OK)

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
    request.data._mutable = True
    # ตรวจสอบค่าที่ส่งมา เช่น emailช้ำ เบอร์ช้ำ
    if request.method == 'POST':
        if request.data['last_name'] == 'admin':
            request.data.update({'user_type': 'ad'})
        serializer = UserexSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_get_detail_api(request, pk):
    try:
        token = request.headers.get('Authorization')
        userAuth = Userex.objects.get(email=token)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if request.method == 'GET':
        userId = Userex.objects.get(pk=pk)
        newDict = UserexSerializer(userId, context={"request": request}).data
        newDict.pop('password')
        return Response(newDict)


@api_view(['POST', 'PATCH', 'DELETE'])
def user_detail_api(request):
    try:
        token = request.headers.get('Authorization')
        userId = Userex.objects.get(email=token)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if request.method == 'POST':
        newDict = UserexSerializer(userId, context={"request": request}).data
        newDict.pop('password')
        return Response(newDict)

    elif request.method == 'PATCH':
        serializer = UserexSerializer(userId, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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


@api_view(['POST'])
def pet_owner_get_api(request, sta):
    try:
        token = request.headers.get('Authorization')
        userId = Userex.objects.get(email=token)
        userSerializer = UserexSerializer(userId)
        petOwnerAll = Pet.objects.all().filter(owner_id=userSerializer.data['user_id'], status=sta)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if request.method == 'POST':
        serializer = PetSerializer(petOwnerAll, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def pet_get_all_api(request):
    if request.method == 'GET':
        petAll = Pet.objects.all().filter(status='nonAdopt')
        serializer = PetSerializer(petAll, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'PATCH', 'POST', 'DELETE'])
def pet_detail_api(request, pk):
    try:
        token = request.headers.get('Authorization')
        Userex.objects.get(email=token)
        petId = Pet.objects.get(pk=pk)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if request.method == 'GET':
        serializer = PetSerializer(petId)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = PetSerializer(petId, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        petId.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Pets images
@api_view(['POST'])
def pet_image_create_api(request):
    if request.method == 'POST':
        try:
            token = request.headers.get('Authorization')
            Userex.objects.get(email=token)
        except Userex.DoesNotExist:
            return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        serializer = PetImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'POST', 'DELETE'])
def pet_images_get_api(request, pk):
    try:
        token = request.headers.get('Authorization')
        Userex.objects.get(email=token)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if request.method == 'GET':
        petImageAll = PetImage.objects.all().filter(pet_id=pk)
        serializer = PetImageSerializer(petImageAll, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        Image = PetImage.objects.get(pk=pk)
        Image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Report
@api_view(['GET'])
def report_all_api(request):
    if request.method == 'GET':
        reportDetailAll = Report.objects.all()
        serializer = SendReportSerializer(reportDetailAll, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def report_detail_api(request, id):
    # try:
    #     token = request.headers.get('Authorization')
    #     userID = Userex.objects.get(email=token)
    # except Userex.DoesNotExist:
    #     return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if request.method == 'GET':
        reportDetail = Report.objects.get(report_id=id)
        reportDetailSerializer = ReportSerializer(reportDetail)
        reporterDetail = Userex.objects.get(user_id=reportDetailSerializer.data['reporter'])
        reporterDetailSerializer = UserexSerializer(reporterDetail, context={"request": request}).data
        reporterDetailSerializer.pop('password')
        reportToDetail = Userex.objects.get(user_id=reportDetailSerializer.data['report_to'])
        reportToDetailSerializer = UserexSerializer(reportToDetail, context={"request": request}).data
        reportToDetailSerializer.pop('password')
        reportPetDetail = Pet.objects.get(pet_id=reportDetailSerializer.data['pet_id'])
        reportPetDetailSerializer = PetSerializer(reportPetDetail)
        reportPetImagesDetail = PetImage.objects.get(pet_id=reportDetailSerializer.data['pet_id'])
        reportPetImagesSerializer = PetImageSerializer(reportPetImagesDetail, context={"request": request})
        newDict = {'reportDetail': reportDetailSerializer.data, 'reporterDetail': reporterDetailSerializer,
                   'reportToDetail': reportToDetailSerializer, 'reportPetDetail': reportPetDetailSerializer.data,
                   'reportPetImagesDetail': reportPetImagesSerializer.data}
        return Response(newDict, status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH'])
def report_user_update_api(request, id):
    if request.method == 'PATCH':
        userDetail = Userex.objects.get(user_id=id)
        userDetail.status = 'off'
        userDetail.save(update_fields=['status'])
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def chat_create_api(request):
    request.data._mutable = True
    if request.method == 'POST':
        try:
            token = request.headers.get('Authorization')
            userId = Userex.objects.get(email=token)
        except Userex.DoesNotExist:
            return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        petId = Pet.objects.get(pet_id=request.data['pet_id'])
        serializerPet = PetSerializer(petId)
        serializerUserex = UserexSerializer(userId)

        try:
            serializerChat = ChatSerializer(
                Chat.objects.get(pet_id=request.data['pet_id'], finder_id=serializerUserex.data['user_id']))
            return Response(serializerChat.data, status=status.HTTP_202_ACCEPTED)
        except Chat.DoesNotExist:
            request.data.update({'owner_id': serializerPet.data['owner_id']})
            request.data.update({'finder_id': serializerUserex.data['user_id']})
            serializer = ChatSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serializerChat = ChatSerializer(
                    Chat.objects.get(pet_id=serializerPet.data['pet_id'], finder_id=serializerUserex.data['user_id']))
                return Response(serializerChat.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_owner_pet_detail(request, id):
    if request.method == 'GET':
        petDetail = Pet.objects.get(pet_id=id)
        petDetailSerializer = PetSerializer(petDetail)
        petImages = PetImage.objects.get(pet_id=id)
        petImagesSerializer = PetImageSerializer(petImages, context={"request": request})
        userDetail = Userex.objects.get(user_id=petDetailSerializer.data['new_owner_id'])
        userDetailSerializer = UserexSerializer(userDetail, context={"request": request}).data
        userDetailSerializer.pop('password')
        newDict = {'PetDetail': petDetailSerializer.data, 'PetImages': petImagesSerializer.data, 'Userdetail': userDetailSerializer}
        return Response(newDict, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def user_owner_send_report(request):
    if request.method == 'POST':
        reportserializer = SendReportSerializer(data=request.data)
        if reportserializer.is_valid():
            reportserializer.save()
            return Response(reportserializer.data, status=status.HTTP_201_CREATED)
        return Response(reportserializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_get_detail(request, id):
    if request.method == 'GET':
        userDetail = Userex.objects.get(user_id=id)
        userSerializer = UserexSerializer(userDetail, context={"request": request}).data
        userSerializer.pop('password')
        return Response(userSerializer, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def chat_detail_api(request, pk):
    try:
        token = request.headers.get('Authorization')
        Userex.objects.get(email=token)
        chatId = Chat.objects.get(pk=pk)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if request.method == 'GET':
        serializer = ChatSerializer(chatId)
        return Response(serializer.data)


@api_view(['POST'])
def chat_get_api(request):
    try:
        token = request.headers.get('Authorization')
        userId = Userex.objects.get(email=token)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    serializerUserex = UserexSerializer(userId)
    chatId = Chat.objects.filter(finder_id=serializerUserex.data['user_id']) | Chat.objects.filter(owner_id=serializerUserex.data['user_id'])
    if request.method == 'POST':
        serializer = ChatSerializer(chatId, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def chat_get_pet_api(request, pk):
    try:
        token = request.headers.get('Authorization')
        userId = Userex.objects.get(email=token)
    except Userex.DoesNotExist:
        return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    chatId = Chat.objects.filter(pet_id=pk)
    if request.method == 'GET':
        serializer = ChatSerializer(chatId, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def message_create_api(request):
    request.data._mutable = True
    if request.method == 'POST':
        try:
            token = request.headers.get('Authorization')
            userId = Userex.objects.get(email=token)
        except Userex.DoesNotExist:
            return Response({'message': 'กรุณาเข้าสู่ระบบ'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        serializerUserex = UserexSerializer(userId)
        request.data.update({'sender_id': serializerUserex.data['user_id']})
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def message_get_by_chat_api(request, pk):
    if request.method == 'GET':
        messageByChat = Message.objects.all().filter(chat_id=pk)
        serializer = MessageSerializer(messageByChat, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
