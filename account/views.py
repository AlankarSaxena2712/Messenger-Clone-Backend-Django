from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes

from .serializers import *
from services.response import *
from .utility import *
from .models import *

User = get_user_model()


@permission_classes((AllowAny,))
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return bad_request_response(serializer.errors)
        check_user = User.objects.all().filter(username=request.data['username'])
        if not check_user:
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
            user.save()
            return create_response({"message": "success"})
        else:
            return bad_request_response({"message": "failure"})


@permission_classes((AllowAny,))
class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return bad_request_response(serializer.errors)
        token = create_token(number=request.data['username'], password=request.data['password'])
        if token:
            return create_response({'token': token.key})
        return bad_request_response({'Message': "Invalid Username or Password!"})


@permission_classes((IsAuthenticated,))
class RoomAPIView(generics.CreateAPIView, generics.RetrieveAPIView):
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(Room.objects.all(), many=True)
        return success_response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated,))
class MessageAPIView(generics.CreateAPIView, generics.RetrieveAPIView):
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(Message.objects.all().filter(room__name=kwargs['room']), many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            room = Room.objects.get(name=kwargs['room'])
            serializer.save(sender=request.user, room=room)
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)
