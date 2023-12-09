import json
from django.core.management.base import BaseCommand
from portfolio.models import Role


class Command(BaseCommand):
    help = 'Import roles from a JSON file'

    def handle(self, *args, **options):
        with open('portfolio/fixtures/roles.json', 'r') as file:
            data = json.load(file)
            for item in data:
                Role.objects.get_or_create(
                    slug=item['slug'],
                    defaults={
                        'name': item['name'],
                        'description': item['description'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported roles'))
