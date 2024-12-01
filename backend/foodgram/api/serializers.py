from rest_framework import serializers

from users.models import User


class ReadUserSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class CreateUserSerializer(serializers.ModelSerializer):
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
