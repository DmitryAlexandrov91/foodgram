"""Кастомные фильтры приложения api."""
from django_filters import rest_framework
from typing import Any

from foodgram.constants import RECIPE_STATUS_CHOICES
from recipes.models import Ingredient, Recipe
from users.models import User


class IngredientFilter(rest_framework.FilterSet):
    """Фильтрация для эндпоина ingredients."""

    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='istartswith')

    class Meta:
        """IngredientFilter метакласс."""

        model = Ingredient
        fields = ('name', )


class RecipeFilter(rest_framework.FilterSet):
    """Фильтрация для эндпоинта recipes."""

    author = rest_framework.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    is_in_shopping_cart = rest_framework.ChoiceFilter(
        choices=RECIPE_STATUS_CHOICES,
        method='get_is_in_shopping_cart'
    )
    is_favorited = rest_framework.ChoiceFilter(
        choices=RECIPE_STATUS_CHOICES,
        method='get_is_favorited'
    )

    def get_is_in_shopping_cart(
            self, queryset: Any, name: str, value: str) -> Any:
        """Фильтрация кверисета по параметру is_in_shopping_cart."""
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                queryset = queryset.filter(shopping_cart__user=user)
        return queryset

    def get_is_favorited(
            self, queryset: Any, name, value: str) -> Any:
        """Фильтрация кверисета по параметру is_favorited."""
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                queryset = queryset.filter(favorite__user=user)
        return queryset

    class Meta:
        """RecipeFilter метакласс."""

        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']
