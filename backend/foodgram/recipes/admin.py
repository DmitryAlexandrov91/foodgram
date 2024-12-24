"""Настройка админ зоны приложения recipes."""
from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    RecipeLinks,
    ShoppingCart,
    Tag)


class IngredientInRecipeInline(admin.StackedInline):
    """Для моделей IngredientAdmin и RecipeAdmin."""

    model = IngredientInRecipe
    extra = 1


class ShoppingCartInline(admin.StackedInline):
    """Для моделей RecipeAdmin и UserAdmin."""

    model = ShoppingCart
    extra = 1


class FavoriteInline(admin.StackedInline):
    """Для моделей RecipeAdmin и UserAdmin."""

    model = Favorite
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка админки модели Ingredient."""

    inlines = (
        IngredientInRecipeInline,
    )

    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка админки модели Recipe."""

    inlines = (
        IngredientInRecipeInline,
        ShoppingCartInline,
        FavoriteInline
    )

    list_display = ('id', 'pub_date', 'name', 'text')
    list_display_links = ('name',)
    fields = ('name', 'author', 'text', 'tags')
    search_fields = ('name', 'author')
    list_filter = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка админки модели Tag."""

    list_display = ('id', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)
    fields = ('name', 'slug')
    filter_horizontal = ('recipe',)


@admin.register(IngredientInRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Настройка админки модели IngredientInRecipe."""

    list_display = ('id', 'ingredient', 'recipe', 'amount')
    list_editable = ('amount',)
    list_display_links = ('recipe',)
    search_fields = ('ingredient',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Настройка админки модели ShoppingCart."""

    list_display = ('id', 'user', 'recipe')
    list_filter = ('user',)
    list_display_links = ('user',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Настройка админки модели Favorite."""

    list_display = ('id', 'user', 'recipe')
    list_display_links = ('recipe',)


@admin.register(RecipeLinks)
class RecipeLinksAdmin(admin.ModelAdmin):
    """Настройка админки модели RecipeLinks."""

    list_display = ('id', 'short_link', 'recipe_id')
    list_display_links = ('short_link',)
