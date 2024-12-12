from django.contrib import admin

from .models import User, Subscribe
from recipes.models import Recipe
from recipes.admin import ShoppingCartInline


class RecipeInline(admin.StackedInline):
    """For UserAdmin model."""

    model = Recipe
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """IngredientAdmin model."""

    inlines = (
        ShoppingCartInline,
        RecipeInline
    )

    list_display = ('id', 'username', 'email')
    list_display_links = ('id',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'author', 'created')
    list_display_links = ('created',)
