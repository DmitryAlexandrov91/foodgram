# Generated by Django 4.2.17 on 2024-12-21 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_recipelinks_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipelinks',
            name='original_link',
        ),
        migrations.AlterField(
            model_name='recipelinks',
            name='short_link',
            field=models.CharField(max_length=5, unique=True, verbose_name='Короткая ссылка'),
        ),
    ]
