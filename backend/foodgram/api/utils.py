"""Вспомогательные функции приложения api."""
import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import status


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


def to_create_del(
        request,
        model_from,
        model_to_save, 
        serializer,
        pk=None):
    """Вспомогательная DRY функция для api views."""
    object_to_action = get_object_or_404(model_from, id=pk)
    if request.method == 'POST':
        serializer = serializer(
            object_to_action,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if model_to_save.objects.filter(
            user=request.user, recipe=object_to_action
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model_to_save.objects.create(
            user=request.user, recipe=object_to_action)
        modified_data = {
            **serializer.data,
            'image': request.build_absolute_uri(
                object_to_action.image.url
            )
        }
        return Response(modified_data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        object = get_object_or_404(
            model_to_save,
            user=request.user,
            recipe=object_to_action
        )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)