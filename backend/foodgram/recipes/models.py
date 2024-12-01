from django.core import validators
from django.db import models

from users.models import User

from api.constants import MIN_COOKING_TIME, MIN_INGREDIENT_QUANITY


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        'Название ингредиента',
        max_length=128

    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=64
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        'Название тэга',
        max_length=32,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг тэга',
        unique=True,
        validators=[validators.RegexValidator(
            regex='^[-a-zA-Z0-9_]+$',
            message='Недопустимый слаг.')]
            )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации рецепта',
        auto_now_add=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Название ингридиента'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    image = models.ImageField(
        'Картинка рецепта',
        upload_to='recipes/',
        blank=True
    )
    name = models.CharField(
        'Название рецепта',
        max_length=256
    )
    text = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(validators.MinValueValidator(
            MIN_COOKING_TIME, 'Не меньше 1 минуты!'),),
        default=MIN_COOKING_TIME
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Favourites(models.Model):
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
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
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
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'


class IngredientRecipe(models.Model):
    """Вспомогательная модель для связи Ингредиентов и Рецептов."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts',
        verbose_name='Рецепт',
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        validators=(validators.MinValueValidator(
            MIN_INGREDIENT_QUANITY, message='Кол-во ингредиентов не менее 1'),),
        default=MIN_INGREDIENT_QUANITY
    )

    class Meta:
        verbose_name = 'ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'В рецепте {self.recipe} есть ингредиент {self.ingredient}'
