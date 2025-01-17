# Generated by Django 4.2.17 on 2024-12-06 08:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_alter_recipe_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favourites',
            new_name='Favorites',
        ),
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='quantity',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='recipes.ingredient', verbose_name='Ингредиенты'),
        ),
    ]
