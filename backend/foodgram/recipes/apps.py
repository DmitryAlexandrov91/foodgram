"""Конфигурация приложения recipes."""
from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """RecipesConfig класс."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
