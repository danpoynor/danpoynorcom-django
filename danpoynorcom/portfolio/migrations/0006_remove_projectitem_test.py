# Generated by Django 5.0 on 2023-12-09 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0005_projectitem_test"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projectitem",
            name="test",
        ),
    ]
