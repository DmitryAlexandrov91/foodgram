from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    IngredientInRecipe,
    Tag,
    ShoppingCart
)


class IngredientInRecipeInline(admin.StackedInline):
    """For IngredientAdmin and RecipeAdmin models."""

    model = IngredientInRecipe
    extra = 1


class ShoppingCartInline(admin.StackedInline):
    """For RecipeAdmibn and UserAdmin models."""

    model = ShoppingCart
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """IngredientAdmin model."""

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
    """RecipeAdmin model."""

    inlines = (
        IngredientInRecipeInline,
        ShoppingCartInline
    )

    list_display = ('id', 'pub_date', 'name', 'text')
    list_display_links = ('name',)
    fields = ('name', 'author', 'text', 'tags')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """TagAdmin model."""

    list_display = ('id', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)
    fields = ('name', 'slug')
    filter_horizontal = ('recipe',)


@admin.register(IngredientInRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """IngredientRecipeAdmin model."""

    list_display = ('id', 'ingredient', 'recipe', 'amount')
    list_editable = ('amount',)
    list_display_links = ('recipe',)
    search_fields = ('ingredient',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'recipe')
    list_filter = ('user',)
    list_display_links = ('user',)
