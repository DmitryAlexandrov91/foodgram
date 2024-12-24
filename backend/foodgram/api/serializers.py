"""Сериализаторы представлений приложения api."""
import base64
import re

from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from foodgram.constants import (
    USERNAME_PATTERN,
    MIN_RECIPE_COOKING_TIME)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag)
from users.models import User, Subscribe


class Base64ImageField(serializers.ImageField):
    """Сериализатор изображения."""

    def to_internal_value(self, data):
        """Преобразовывает входные данные для сохранения изображений."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара пользователя."""

    avatar = Base64ImageField()

    class Meta:
        """AvatarSerializer метакласс."""

        model = User
        fields = ['avatar',]

    def update(self, instance, validated_data):
        """Поведение бновления аватара при put запросе."""
        instance.avatar = validated_data.get(
            'avatar')
        instance.save()
        return instance


class ReadUserSerializer(UserSerializer):
    """Сериализатор для чтения пользователя."""

    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        """ReadUserSerializer метакласс."""

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
        """Получет кверисет из модели Subscribe."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=request.user,
            author=obj).exists()


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        """CreateUserSerializer метакласс."""

        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
        required_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def validate_username(self, value):
        """Валидация поля username."""
        is_mutch = (re.match(
            USERNAME_PATTERN,
            value))
        if not is_mutch:
            raise ValidationError(f'Имя пользователя {value} недопустимо!')
        if User.objects.filter(username=value).exists():
            raise ValidationError(
                f'Имя пользователя {value} уже зарегистрировано.',
            )
        return value

    def validate_email(self, value):
        """Валидация поля email."""
        if User.objects.filter(email=value).exists():
            raise ValidationError(
                f'Email {value} уже зарегистрирован.'
            )
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор смены пароля пользователя."""

    current_password = serializers.CharField()
    new_password = serializers.CharField()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тэгов."""

    class Meta:
        """TagSerializer метакласс."""

        model = Tag
        fields = '__all__'
        read_only_fields = ['__all__',]


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов."""

    class Meta:
        """IngredientSerializer метакласс."""

        model = Ingredient
        fields = '__all__'


class ReadIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели IngredientInRecipe."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        """ReadIngredientInRecipeSerializer метакласс."""

        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""

    tags = TagSerializer(
        many=True,
    )
    author = ReadUserSerializer()
    ingredients = ReadIngredientInRecipeSerializer(
        many=True,
        source='recipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        """ReadRecipeSerializer метакласс."""

        model = Recipe
        exclude = ['pub_date']

    def get_is_favorited(self, obj):
        """Возвращает True или False если объект в избранном."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj,
                                       user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        """Возвращает True или False если объект в корзине покупок."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class CreateIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для записи модели IngredientInRecipe."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        """CreateIngredientInRecipeSerializer метакласс."""

        model = IngredientInRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Серилизатор для создания рецепта."""

    image = Base64ImageField()
    ingredients = CreateIngredientInRecipeSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        """CreateRecipeSerializer метакласс."""

        model = Recipe
        exclude = ['pub_date']
        read_only_fields = ('author',)

    def validate(self, data):
        """Валидация данных сериализатора на наличие тэгов и ингредиентов."""
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            if 'tags' not in data:
                raise serializers.ValidationError(
                    'В запросе нет поля tags!')
            if "ingredients" not in data:
                raise serializers.ValidationError(
                    'В запросе нет поля ingredients!')
        return data

    def validate_ingredients(self, value):
        """Валидация поля ingredients."""
        if not value:
            raise ValidationError('Рецепт не может быть без ингредиентов!')
        if any(value.count(item) > 1 for item in value):
            raise ValidationError('Ингредиенты не должны повторяться!')
        return value

    def validate_tags(self, value):
        """Валидация поля tags."""
        if not value:
            raise ValidationError('Необходимо выбрать хотя бы один тег!')
        if any(value.count(item) > 1 for item in value):
            raise ValidationError('Теги не должны повторяться!')
        return value

    def validate_cooking_time(self, value):
        """Валидация поля cooking_time."""
        if value < MIN_RECIPE_COOKING_TIME:
            raise ValidationError(
                'Время приготовление рецепта не может быть меньше '
                f'{MIN_RECIPE_COOKING_TIME}')
        return value

    def create_ingredient_in_recipe(self, ingredients, recipe):
        """Вспомогательная функция для записи списка объектов в модель."""
        IngredientInRecipe.objects.bulk_create(
            [IngredientInRecipe(
                ingredient=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount')
            ) for ingredient in ingredients])

    def create(self, validated_data):
        """Поведение при создании рецепта."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredient_in_recipe(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        """Поведение при обновлении рецепта."""
        recipe = instance
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.clear()
        instance.ingredients.clear()
        tags = validated_data.get('tags')
        instance.tags.set(tags)
        ingredients = validated_data.get('ingredients')
        IngredientInRecipe.objects.filter(recipe=recipe).delete()
        self.create_ingredient_in_recipe(ingredients, recipe)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Переопределяет вид ответа от api."""
        return ReadRecipeSerializer(instance, context={
            'request': self.context.get('request')}
        ).data


class ShoppingCartAndFavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного и корзины покупок."""

    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        """ShoppingCartAndFavoriteSerializer метакласс."""

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(ReadUserSerializer):
    """Сериализатор для подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        """SubscribeSerializer метакласс."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar'
        )

    def get_recipes(self, obj):
        """Ограничивает выдачу рецептов по параметру recipes_limit."""
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            try:
                limit = int(recipes_limit)
                recipes = Recipe.objects.filter(
                    author=obj)[:limit]
            except ValueError:
                recipes = Recipe.objects.filter(
                    author=obj)
        else:
            recipes = Recipe.objects.filter(
                author=obj
            )
        context = {'request': request}
        return ShoppingCartAndFavoriteSerializer(
            recipes,
            many=True,
            context=context).data

    def get_recipes_count(self, obj):
        """Определяет ззначение поля recipes_count."""
        return Recipe.objects.filter(author=obj).count()
