import base64

from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.core.files.base import ContentFile

from users.models import User, Subscribe
from recipes.models import Tag, Recipe, IngredientInRecipe, Ingredient


class Base64ImageField(serializers.ImageField):
    """Изображения."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = ['avatar', 'image_url']

    def get_image_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get(
            'avatar', self.get_image_url(instance)
        )
        instance.image_url = self.get_image_url(instance)
        instance.save()
        return instance


class ReadUserSerializer(UserSerializer):
    """Сериализатор на чтение пользователя."""
    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )

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
        try:
            if request.user.is_anonymous:
                return False
        except AttributeError:
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


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['__all__',]


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор вспомогательной модели рецептов и ингредиентов."""
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
        )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""
    tags = TagSerializer(
        many=True,
    )
    author = ReadUserSerializer()
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='recipe'
    )

    class Meta:
        model = Recipe
        exclude = ['pub_date']
