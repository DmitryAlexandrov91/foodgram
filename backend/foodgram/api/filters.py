from django_filters import rest_framework as filters


from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    """Фильтрация для эндпоина ingredients."""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
