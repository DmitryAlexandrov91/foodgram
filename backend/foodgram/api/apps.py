"""Конфигурация приложение api."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """ApiConfig класс."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
