from django.core import validators
from django.db import models

from users.models import User

MIN_COOKING_TIME = 1


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        'Название ингредиента',
        unique=True,
        max_length=128

    )
    measurement_unit = models.CharField(
        'Единица измерения',
        unique=True,
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
        verbose_name='Название ингридиента',
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
        validators=(validators.MinValueValidator(MIN_COOKING_TIME, 'Не меньше 1 минуты!'),),
        default=MIN_COOKING_TIME
    )



