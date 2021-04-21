from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *
from services.serialzers import ForeignKeyField


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(required=True, max_length=50)

    class Meta:
        fields = [
            'username',
            'password'
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=10)
    password = serializers.CharField(required=True, max_length=75)

    class Meta:
        fields = [
            'username',
            'password'
        ]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'name'
        ]
        read_only_fields = ['id']


class MessageSerializer(serializers.ModelSerializer):
    sender = ForeignKeyField(queryset=User.objects, filter_by='username', required=False)
    room = ForeignKeyField(queryset=Room.objects, filter_by='name', required=False)
    class Meta:
        model = Message
        fields = [
            'id',
            'content',
            'sender',
            'room'
        ]
        read_only_fields = ['id', 'sender', 'room']
