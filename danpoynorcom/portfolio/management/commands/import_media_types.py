import json
from django.core.management.base import BaseCommand
from portfolio.models import MediaType


class Command(BaseCommand):
    help = 'Import media types from a JSON file'

    def handle(self, *args, **options):
        with open('portfolio/fixtures/media_types.json', 'r') as file:
            data = json.load(file)
            for item in data:
                MediaType.objects.get_or_create(
                    slug=item['slug'],
                    defaults={
                        'name': item['name'],
                        'description': item['description'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported media types'))
