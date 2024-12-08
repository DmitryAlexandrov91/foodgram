from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    IngredientInRecipe,
    Tag
)


class IngredientRecipeInline(admin.StackedInline):
    """For IngredientAdmin model."""

    model = IngredientInRecipe
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """IngredientAdmin model."""

    inlines = (
        IngredientRecipeInline,
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
        IngredientRecipeInline,
    )

    list_display = ('id', 'pub_date', 'name', 'text')
    list_display_links = ('name',)
    fields = ('name', 'author', 'text', 'tags')
    filter_horizontal = ('ingredients',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """TagAdmin model."""

    list_display = ('id', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)
    filter_horizontal = ('recipe',)


@admin.register(IngredientInRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """IngredientRecipeAdmin model."""

    list_display = ('id', 'ingredient', 'recipe', 'amount')
    list_editable = ('amount',)
    list_display_links = ('recipe',)
    search_fields = ('ingredient',)
