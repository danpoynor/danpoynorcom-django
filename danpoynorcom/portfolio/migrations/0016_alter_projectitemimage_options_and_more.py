# Generated by Django 5.0 on 2023-12-21 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0015_alter_projectitemattachment_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="projectitemimage",
            options={
                "verbose_name": "Project Image",
                "verbose_name_plural": "Project Images",
            },
        ),
        migrations.AlterModelTable(
            name="projectitemimage",
            table="portfolio_project_item_image",
        ),
    ]
