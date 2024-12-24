"""Кастомные пагинаторы проекта Foodgram."""
from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    """Пагинация главной страниый recipes."""

    page_size = 6
    page_size_query_param = 'limit'
