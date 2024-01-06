import re
from django.db import migrations


def correct_image_extensions(apps, schema_editor):
    # Get the model from the versioned app registry to ensure the correct version is used
    ProjectItem = apps.get_model('portfolio', 'ProjectItem')

    # Update the html_content field of each ProjectItem
    for item in ProjectItem.objects.all():
        item.html_content = re.sub(r'(src="[^"]*)\.(png|jpg)\.webp', r'\1.webp', item.html_content, flags=re.IGNORECASE)
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0025_update_content_png_jpeg_images_to_webp'),  # Replace with the name of the previous migration
    ]

    operations = [
        migrations.RunPython(correct_image_extensions, migrations.RunPython.noop),
    ]
