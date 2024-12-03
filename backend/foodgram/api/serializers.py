from django.contrib.auth import authenticate
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from users.models import User


class ReadUserSerializer(UserSerializer):
    """Сериализатор на чтение пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор на создание пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        required_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
