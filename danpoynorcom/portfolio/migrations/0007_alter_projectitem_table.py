# Generated by Django 5.0 on 2023-12-09 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0006_remove_projectitem_test"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="projectitem",
            table="portfolio_project_item",
        ),
    ]
