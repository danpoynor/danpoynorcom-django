# fmt: off

import os
import re
import sys
import django

# Add the parent directory of the script's directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'danpoynorcom.settings')
django.setup()

# Import the ProjectItem model after setting up Django
from portfolio.models import ProjectItem

# Fetch all ProjectItems
items = ProjectItem.objects.all()

# Define a regex pattern to match image filenames
pattern = re.compile(r'(?P<filename>[a-zA-Z0-9_-]+\.(jpg|jpeg|gif|png))')

# Initialize a set to store unique image filenames
image_filenames = set()

# Iterate over all items
for item in items:
    # Find all image filenames in the item's html_content
    matches = pattern.findall(item.html_content)
    # Add each filename to the set
    for match in matches:
        image_filenames.add(match[0])

# Open a file in write mode
with open('image_filenames.txt', 'w', encoding='utf-8') as f:
    # Write each filename to the file
    for filename in image_filenames:
        f.write(filename + '\n')

# fmt: on
