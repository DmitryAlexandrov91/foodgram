import base64

from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.core.files.base import ContentFile
from rest_framework.relations import SlugRelatedField

from users.models import User, Subscribe
from recipes.models import Tag, Recipe, IngredientInRecipe, Ingredient, Favorite, ShoppingCart


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
    """Сериализатор для чтения пользователя."""

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
    """Сериализатор для создания пользователя."""

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
    """Сериализатор модели тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['__all__',]


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class ReadIngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения вспомогательной модели рецептов и ингредиентов.
    """

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
        )

    class Meta:
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
        source='ingredientinrecipe_recipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ['pub_date']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj,
                                       user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class CreateIngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для записи вспомогательной модели рецептов и ингредиентов.
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Серилизатор для создания рецепта."""

    image = Base64ImageField()
    ingredients = CreateIngredientInRecipeSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        exclude = ['pub_date']
        read_only_fields = ('author',)

    def create_ingredient_in_recipe(self, ingredients, recipe):
        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    ingredient=ingredient.get('id'),
                    recipe=recipe,
                    amount=ingredient.get('amount')
                    )
                for ingredient in ingredients
                ]
                )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredient_in_recipe(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        recipe = instance
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time)
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
        return ReadRecipeSerializer(instance, context={
            'request': self.context.get('request')}
            ).data

