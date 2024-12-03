from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from users.models import User


class ReadUserSerializer(UserSerializer):
    """Сериализатор на чтение пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
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

    def to_representation(self, instance):
        return ReadUserSerializer(instance).data
