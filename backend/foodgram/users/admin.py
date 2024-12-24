"""Настройка админ зоны приложения users."""
from django.contrib import admin

from recipes.admin import FavoriteInline, ShoppingCartInline
from recipes.models import Recipe
from .models import Subscribe, User


class RecipeInline(admin.StackedInline):
    """Для модели UserAdmin."""

    model = Recipe
    extra = 1


class FollowerInline(admin.StackedInline):
    """Для модели UserAdmin."""

    model = Subscribe
    fk_name = "user"


class SubscribedAuthorInline(admin.StackedInline):
    """Для модели UserAdmin."""

    model = Subscribe
    fk_name = "author"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка админки модели User."""

    inlines = (
        ShoppingCartInline,
        RecipeInline,
        FavoriteInline,
        FollowerInline,
        SubscribedAuthorInline
    )

    list_display = ('id', 'username', 'email')
    list_display_links = ('username',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Настройка админки модели Subscribe."""

    list_display = ('id', 'user', 'author', 'created')
    list_display_links = ('created',)
