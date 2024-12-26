"""Модели приложения recipes."""
from django.core import validators
from django.db import models
from django.dispatch import receiver
import shortuuid

from foodgram.constants import (
    MIN_RECIPE_COOKING_TIME,
    MIN_RECIPE_INGREDIENT_QUANITY,
    MAX_RECIPE_NAME_LENGHT,
    MAX_RECIPELINKS_SHORTLINK_LENGHT,
    MAX_INGREDIENT_MEASUREMENT_UNIT_LENGHT,
    MAX_INGREDIENT_NAME_LENGHT,
    MAX_TAG_NAME_LENGHT,
    TAG_SLUG_REGEX)
from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        'Название ингредиента',
        max_length=MAX_INGREDIENT_NAME_LENGHT

    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_INGREDIENT_MEASUREMENT_UNIT_LENGHT
    )

    class Meta:
        """Ingredient метакласс."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        """Возвращает называние ингредиента и его ед. измерения."""
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        'Название тэга',
        max_length=MAX_TAG_NAME_LENGHT,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг тэга',
        unique=True,
        validators=[validators.RegexValidator(
            regex=TAG_SLUG_REGEX,
            message='Недопустимый слаг.')]
    )

    class Meta:
        """Tag метакласс."""

        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Возвращает название тега."""
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author'
    )
    pub_date = models.DateTimeField(
        'Дата публикации рецепта',
        auto_now_add=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientInRecipe',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    image = models.ImageField(
        'Картинка рецепта',
        upload_to='recipes/images',
        blank=True
    )
    name = models.CharField(
        'Название рецепта',
        max_length=MAX_RECIPE_NAME_LENGHT
    )
    text = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(validators.MinValueValidator(
            MIN_RECIPE_COOKING_TIME, 'Не меньше 1 минуты!'),),
        default=MIN_RECIPE_COOKING_TIME
    )

    class Meta:
        """Recipe метакласс."""

        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Возвращает название рецепта."""
        return self.name


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite'
    )

    class Meta:
        """Favorite метакласс."""

        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        """Возвращает название рецепта и юзерннейм юзера."""
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart'
    )

    class Meta:
        """ShoppingCart метакласс."""

        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        """Возвращает название рецепта и юзернейм юзера."""
        return f'"{self.recipe}" в списке покупок у {self.user}'


class IngredientInRecipe(models.Model):
    """Вспомогательная модель для связи Ингредиентов и Рецептов."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(validators.MinValueValidator(
            MIN_RECIPE_INGREDIENT_QUANITY,
            message='Кол-во ингредиентов не менее 1 ед.'
        ),
        ),
        default=MIN_RECIPE_INGREDIENT_QUANITY,
    )

    class Meta:
        """IngredientInRecipe метакласс."""

        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        """Вовзращает id рецпта и его название."""
        return f'№{self.recipe.id} "{self.recipe.name}"'


class RecipeLinks(models.Model):
    """Модель для хранения ссылок."""

    short_link = models.CharField(
        'Короткая ссылка',
        max_length=MAX_RECIPELINKS_SHORTLINK_LENGHT,
        unique=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    class Meta:
        """RecipeLinks метакласс."""

        verbose_name = 'ссылки'
        verbose_name_plural = 'ссылки'

    def __str__(self):
        """Взвращает короткую ссылку."""
        return self.short_link

    @receiver(models.signals.post_save, sender=Recipe)
    def get_short_link(sender, instance, created, **kwargs):
        """Создаёт короткую ссылку при создании рецепта."""
        if created:
            RecipeLinks.objects.create(
                short_link=shortuuid.ShortUUID().random(
                    length=MAX_RECIPELINKS_SHORTLINK_LENGHT),
                recipe_id=instance.id
            )
