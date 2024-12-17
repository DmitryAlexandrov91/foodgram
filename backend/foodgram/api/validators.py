"""Валдиаторы приложения api."""
from django.core.exceptions import ValidationError


def validate_ingredients(value):
    if not value:
        raise ValidationError('Рецепт не может быть без ингредиентов!')
    if any(value.count(item) > 1 for item in value):
        raise ValidationError('Ингредиенты не должны повторяться!')
    return value
