from django.contrib import admin

from .models import(
    Ingredient,
    Recipe,
    Tag
)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """IngredientAdmin model."""

    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """RecipeAdmin model."""

    list_display = ('id', 'pub_date', 'name', 'text')
    list_display_links = ('name',)
    list_editable = ('text',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """TagAdmin model."""

    list_display = ('id', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)