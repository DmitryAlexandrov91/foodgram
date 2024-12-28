"""Вспомогательные функции приложения api."""
import csv

from django.http import HttpResponse


def get_report_responce(ingredients):
    """Вспомогательная функция для выдачи корзины покупок."""
    shopping_cart = [(
        i["ingredient__name"],
        i["ingredient__measurement_unit"],
        i["amount"],
        i["recipe__name"]) for i in ingredients
    ]
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
        ['Ингредиент', 'Единица измерения',
            'Количество', 'Рецепт'])
    for ingredient in shopping_cart:
        writer.writerow(ingredient)
    return response
