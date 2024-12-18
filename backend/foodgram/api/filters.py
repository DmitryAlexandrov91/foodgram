from django_filters import rest_framework

from recipes.models import Ingredient, Recipe
from users.models import User

from foodgram.constants import RECIPE_STATUS_CHOICES


class IngredientFilter(rest_framework.FilterSet):
    """Фильтрация для эндпоина ingredients."""

    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(rest_framework.FilterSet):
    """Фильтрация для эндпоинта recipes."""

    author = rest_framework.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Ссылка'
    )

    is_in_shopping_cart = rest_framework.ChoiceFilter(
        choices=RECIPE_STATUS_CHOICES,
        method='get_is_in'
    )
    is_favorited = rest_framework.ChoiceFilter(
        choices=RECIPE_STATUS_CHOICES,
        method='get_is_in'
    )

    def get_is_in(self, queryset, name, value):

        print(name)
        print(value)
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                if name == 'is_favorited':
                    queryset = queryset.filter(favorite__user=user)
                if name == 'is_in_shopping_cart':
                    queryset = queryset.filter(shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']
