"""App for db load."""
import csv

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command class."""

    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        """Add csv file path as argument."""
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        """To content db handler."""
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
