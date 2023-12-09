# import_markets.py
import json
from django.core.management.base import BaseCommand
from portfolio.models import Market


class Command(BaseCommand):
    help = 'Import markets from a JSON file'

    def handle(self, *args, **options):
        with open('portfolio/fixtures/markets.json', 'r') as file:
            data = json.load(file)
            for item in data:
                Market.objects.get_or_create(
                    slug=item['slug'],
                    defaults={
                        'name': item['name'],
                        'description': item['description'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported markets'))
