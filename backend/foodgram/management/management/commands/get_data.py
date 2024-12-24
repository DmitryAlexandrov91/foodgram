"""Приложение для загрузки данных в бд."""
import csv

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Класс Command."""

    help = 'Название модели должно полностью совпадать с названием файла csv'

    def add_arguments(self, parser):
        """Добавляет csv файл как аргумент."""
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        """Хэндлер для заполнения БД."""
        models = apps.get_models()
        name = options['path'].split('/')[-1].split('.')[0]
        for model in models:
            if name == model.__name__.lower():
                with open(options['path'], 'r', encoding='utf-8') as csvfile:
                    rows = list(csv.reader(csvfile, delimiter=','))
                    for row in rows[1:]:
                        db = dict(zip(rows[0], row))
                        model.objects.create(**db)
                break
