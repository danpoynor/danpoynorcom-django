import os
import shutil

# Define the source and destination directories
source_dir = '/Users/danpoynor/Development/my-projects/my-sites/portfolio-sites/danpoynor_static/uploads-all-sizes/'
destination_dir = '/Users/danpoynor/Development/my-projects/my-sites/portfolio-sites/danpoynorcom-django/danpoynorcom/portfolio/static/portfolio/images/content/'

# Define the path to the file with image filenames
filename_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image_filenames.txt')

# Open the file with image filenames
with open(filename_path, 'r', encoding='utf-8') as f:
    # Read the image filenames from the file
    image_filenames = [line.strip() for line in f]

# Iterate over all image filenames
for filename in image_filenames:
    # Define the source and destination paths
    source_path = source_dir + filename
    destination_path = destination_dir + filename

    # Check if the file exists in the source directory
    if not os.path.exists(source_path):
        print(f"File not found in source directory: {filename}")
        continue

    # Check if the file already exists in the destination directory
    if os.path.exists(destination_path):
        print(f"File already exists in destination directory: {filename}")
        continue  # Skip copying the file

    # Copy the image from the source path to the destination path
    shutil.copy(source_path, destination_path)
