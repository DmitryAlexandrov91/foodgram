from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe
from users.models import User


class IngredientFilter(filters.FilterSet):
    """Фильтрация для эндпоина ingredients."""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(filters.FilterSet):
    """Фильтрация для эндпоинта recipes."""

    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Ссылка'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
