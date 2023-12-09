import json
import os
from django.core.management.base import BaseCommand
from portfolio.models import Project, ProjectItem


class Command(BaseCommand):
    help = 'Import project items from JSON files'

    def handle(self, *args, **options):
        # Create a default Project instance
        default_project, created = Project.objects.get_or_create(
            name='[Default Project]',
            defaults={
                # Set other fields of the Project instance as needed
            }
        )

        for i in range(1, 20):  # Loop over the numbers 1 to 19
            file_name = f'portfolio/fixtures/portfolio_items_{i:02}.json'  # Generate the file name
            print(f"Looking for file: {file_name}")  # Print the file name
            if os.path.exists(file_name):  # Check if the file exists
                print(f"Found file: {file_name}")  # Print a success message
                with open(file_name, 'r') as file:
                    data = json.load(file)
                    print(f"File {file_name} contains JSON data")  # Print a success message
                    for item in data:
                        print(f"Processing item with slug {item['slug']}")  # Print the slug of the item being processed
                        project_item, created = ProjectItem.objects.get_or_create(
                            slug=item['slug'],
                            defaults={
                                'name': item['title']['rendered'],
                                'status': item['status'].upper()[0],
                                'html_content': item['content']['rendered'],
                                'project': default_project,  # Assign the default Project instance
                            }
                        )
        self.stdout.write(self.style.SUCCESS('Successfully imported project items'))
