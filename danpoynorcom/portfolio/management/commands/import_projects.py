import json
import os
from django.core.management.base import BaseCommand
from portfolio.models import Project


class Command(BaseCommand):
    help = 'Import projects from JSON files'

    def handle(self, *args, **options):
        for i in range(1, 7):  # Loop over the numbers 1 to 6
            file_name = f'portfolio/fixtures/projects_0{i}.json'  # Generate the file name
            if os.path.exists(file_name):  # Check if the file exists
                with open(file_name, 'r') as file:
                    data = json.load(file)
                    for item in data:
                        Project.objects.get_or_create(
                            slug=item['slug'],
                            defaults={
                                'name': item['name'],
                                'description': item['description'],
                            }
                        )
        self.stdout.write(self.style.SUCCESS('Successfully imported projects'))
