"""Кастомные пагинаторы проекта Foodgram."""
from rest_framework.pagination import PageNumberPagination

from foodgram.constants import MAX_RECIPE_PER_PAGE


class RecipePagination(PageNumberPagination):
    """Пагинация для рецептов на главной странице."""

    page_size = MAX_RECIPE_PER_PAGE
    page_size_query_param = 'limit'
