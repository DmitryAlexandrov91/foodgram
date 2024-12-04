import base64

from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.core.files.base import ContentFile

from users.models import User, Subscribe


class Base64ImageField(serializers.ImageField):
    """Изображения."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ['avatar']

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar
        return data


class ReadUserSerializer(UserSerializer):
    """Сериализатор на чтение пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=request.user,
            author=obj
        ).exists()


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
