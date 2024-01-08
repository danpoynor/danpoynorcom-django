from django.conf import settings
import os
import re
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Find potentially unused CSS classes'

    def handle(self, *args, **options):
        # Get all CSS classes from your CSS file
        css_file_path = os.path.join(settings.STATICFILES_DIRS[0], 'portfolio/styles.css')
        with open(css_file_path, 'r', encoding='utf-8') as f:
            css = f.read()

        # Initialize an empty set to store the CSS classes
        css_classes = set()

        # Use a regular expression to find all selectors in the CSS file
        selectors = re.findall(r'}\s*([^{}]*?)\s*{', css, re.MULTILINE | re.DOTALL)

        # Loop over each selector
        for selector in selectors:
            # Split the selector on spaces and commas to get the individual parts of the selector
            parts = re.split(r'[ ,]+', selector)

            # Loop over each part of the selector
            for part in parts:
                # Use a regular expression to find all class names in the part
                classes = re.findall(r'\.([a-zA-Z_-][a-zA-Z0-9_-]*)', part)

                # Add the found classes to the set of CSS classes
                css_classes.update(classes)

        self.stdout.write(f'Found {len(css_classes)} CSS classes in the CSS file.')

        # Get all classes used in your HTML templates
        html_classes = set()
        html_files_count = 0
        for templates_dir in settings.TEMPLATES[0]['DIRS']:
            for dirpath, dirnames, filenames in os.walk(templates_dir):
                for filename in filenames:
                    if filename.endswith('.html'):
                        html_files_count += 1
                        with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as f:
                            html = f.read()

                            # Find all class attributes in the HTML file
                            class_attributes = re.findall(r'class=[\'"](.*?)[\'"]', html)

                            # Split the class attributes into individual classes and add them to the set of HTML classes
                            for class_attribute in class_attributes:
                                html_classes.update(class_attribute.split())

        self.stdout.write(f'Parsed {html_files_count} HTML template files.')
        self.stdout.write(f'Found {len(html_classes)} classes in the HTML templates.')

        # Find the difference between the two sets
        unused_classes = css_classes - html_classes

        self.stdout.write('Potentially unused CSS classes:')
        for unused_class in unused_classes:
            self.stdout.write(f'.{unused_class}')
