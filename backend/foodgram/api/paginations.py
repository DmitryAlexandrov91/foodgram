"""Кастомные пагинаторы проекта Foodgram."""
from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    """Пагинация для рецептов на главной странице."""

    page_size = 6
    page_size_query_param = 'limit'
