import os
import shutil
from urllib.parse import urlparse
from django.conf import settings
from django.core.management.base import BaseCommand
from portfolio.models import ProjectItemImage


class Command(BaseCommand):
    help = 'Moves image files for "images/uploads-all-sizes/" to appropriate directories based on their sizes'

    def handle(self, *args, **options):
        # Get all ProjectItemImage instances
        images = ProjectItemImage.objects.all()

        # Iterate over the ProjectItemImage instances
        for image in images:
            # Replace 'http://danpoynor.com.localhost/wp-content/uploads/' with '' in original
            image.original = image.original.replace('http://danpoynor.com.localhost/wp-content/uploads/', '')
            # Save the ProjectItemImage instance
            image.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated original field of ProjectItemImage instances'))

        # Log the number of image instances found
        self.stdout.write(self.style.SUCCESS(f'Found {images.count()} image instances'))

        # Define the source directory and the target directories
        source_dir = os.path.join(settings.BASE_DIR, 'portfolio/static/portfolio/images/uploads-all-sizes')
        target_dirs = {
            'thumbnail': os.path.join(settings.BASE_DIR, 'portfolio/static/portfolio/images/project-item-images/thumbnail'),
            'medium': os.path.join(settings.BASE_DIR, 'portfolio/static/portfolio/images/project-item-images/medium'),
            'medium_large': os.path.join(settings.BASE_DIR, 'portfolio/static/portfolio/images/project-item-images/medium-large'),
            'large': os.path.join(settings.BASE_DIR, 'portfolio/static/portfolio/images/project-item-images/large'),
            'admin_list_thumb': os.path.join(settings.BASE_DIR, 'portfolio/static/portfolio/images/project-item-images/admin_list_thumb'),
            'original': os.path.join(settings.BASE_DIR, 'portfolio/static/portfolio/images/project-item-images/original'),
        }

        # Iterate over the ProjectItemImage instances
        for image in images:
            # Iterate over the fields in the ProjectItemImage model
            for field_name, target_dir in target_dirs.items():
                # Get the filename from the field
                url = getattr(image, field_name)

                # Check if url is None or doesn't contain a valid path, if so, skip
                if not url or not urlparse(url).path:
                    continue

                filename = os.path.basename(urlparse(url).path)

                # Check if filename is empty, if so, skip
                if not filename:
                    continue

                # Define the source and destination paths
                source_path = os.path.join(source_dir, filename)
                destination_path = os.path.join(target_dir, filename)

                # Log the source and destination paths
                # self.stdout.write(self.style.SUCCESS(f'Source path: {source_path}'))
                # self.stdout.write(self.style.SUCCESS(f'Destination path: {destination_path}'))

                # Try to open the source file in read mode and the destination file in write mode
                try:
                    with open(source_path, 'r') as source_file, open(destination_path, 'w') as destination_file:
                        pass
                except IOError as e:
                    self.stdout.write(self.style.ERROR(f'Failed to open file: {e}'))
                    continue

                # If the source path is not a file, skip
                if not os.path.isfile(source_path):
                    continue

                # If the destination file already exists, delete it
                if os.path.exists(destination_path):
                    os.remove(destination_path)

                # Move the image file to the target directory
                try:
                    shutil.move(source_path, destination_path)
                    # Check if the file exists at the destination path
                    # if os.path.isfile(destination_path):
                    #     self.stdout.write(self.style.SUCCESS(f'Successfully moved file: {filename} to {destination_path}'))
                except FileNotFoundError:
                    self.stdout.write(self.style.ERROR(f'File not found: {filename}'))

        self.stdout.write(self.style.SUCCESS('Finished moving image files'))
