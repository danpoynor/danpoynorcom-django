# Generated by Django 5.0 on 2023-12-21 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0016_alter_projectitemimage_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="projectitemattachment",
            old_name="is_visible",
            new_name="visible",
        ),
    ]
