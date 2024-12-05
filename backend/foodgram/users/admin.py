from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """IngredientAdmin model."""

    list_display = ('id', 'username', 'email')
    list_display_links = ('id',)
