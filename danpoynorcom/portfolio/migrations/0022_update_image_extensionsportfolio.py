from django.db import migrations


def update_image_extensions(apps, schema_editor):
    ProjectItemImage = apps.get_model("portfolio", "ProjectItemImage")
    for item in ProjectItemImage.objects.all():
        if item.thumbnail.endswith(".gif") or item.thumbnail.endswith(".jpg") or item.thumbnail.endswith(".png"):
            item.thumbnail = item.thumbnail.rsplit(".", 1)[0] + ".webp"
            item.save()
        if item.medium.endswith(".gif") or item.medium.endswith(".jpg") or item.medium.endswith(".png"):
            item.medium = item.medium.rsplit(".", 1)[0] + ".webp"
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0021_alter_client_visible_alter_industry_visible_and_more"),
    ]

    operations = [
        migrations.RunPython(update_image_extensions),
    ]
