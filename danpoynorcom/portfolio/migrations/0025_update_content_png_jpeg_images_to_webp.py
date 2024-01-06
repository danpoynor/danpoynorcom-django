import re
from django.db import migrations


def replace_image_extensions(apps, schema_editor):
    # Get the model from the versioned app registry to ensure the correct version is used
    ProjectItem = apps.get_model('portfolio', 'ProjectItem')

    # Update the html_content field of each ProjectItem
    for item in ProjectItem.objects.all():
        item.html_content = re.sub(r'(src="[^"]*\.(png|jpg|jpeg))', r'\1.webp', item.html_content, flags=re.IGNORECASE)
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0024_update_image_paths_2'),  # Replace with the name of the previous migration
    ]

    operations = [
        migrations.RunPython(replace_image_extensions),
    ]
