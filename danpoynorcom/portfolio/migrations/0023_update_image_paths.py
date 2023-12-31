from django.db import migrations, models
from django.db.models import F


def replace_image_paths(apps, schema_editor):
    # Get the model from the versioned app registry to ensure the correct version is used
    ProjectItem = apps.get_model('portfolio', 'ProjectItem')

    # Update the html_content field of each ProjectItem
    for item in ProjectItem.objects.all():
        item.html_content = item.html_content.replace('http://danpoynor.com.localhost/wp-content/uploads/', '/static/portfolio/images/content/')
        item.html_content = item.html_content.replace('/wp-content/themes/danpoynor-2017/images/adteractive-email-images/', '/static/portfolio/images/adteractive-email-images/')
        item.html_content = item.html_content.replace('/wp-content/themes/danpoynor-2017/images/adteractive-landing-page-images/', '/static/portfolio/images/adteractive-landing-page-images/')
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0022_update_image_extensionsportfolio'),  # Replace with the name of the previous migration
    ]

    operations = [
        migrations.RunPython(replace_image_paths),
    ]
