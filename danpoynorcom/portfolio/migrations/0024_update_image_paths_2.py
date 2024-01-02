from django.db import migrations


def replace_image_paths(apps, schema_editor):
    # Get the model from the versioned app registry to ensure the correct version is used
    ProjectItem = apps.get_model('portfolio', 'ProjectItem')

    # Update the html_content field of each ProjectItem
    for item in ProjectItem.objects.all():
        item.html_content = item.html_content.replace('/wp-content/uploads//', '/static/portfolio/images/content/')
        item.html_content = item.html_content.replace('/wp-content/uploads/', '/static/portfolio/images/content/')
        item.html_content = item.html_content.replace('/wp-content/themes/danpoynor-2017/images/imvu-email-images/', '/static/portfolio/images/imvu-email-images/')
        item.html_content = item.html_content.replace('/wp-content/themes/danpoynor-2017/images/oxiclean/', '/static/portfolio/images/oxiclean/')
        item.html_content = item.html_content.replace('/wp-content/themes/danpoynor-2017/images/flash/', '/static/portfolio/flash/')
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0023_update_image_paths'),  # Replace with the name of the previous migration
    ]

    operations = [
        migrations.RunPython(replace_image_paths),
    ]
