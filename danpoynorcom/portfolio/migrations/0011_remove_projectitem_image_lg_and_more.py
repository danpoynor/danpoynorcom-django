# Generated by Django 5.0 on 2023-12-18 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0010_projectitem_item_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projectitem",
            name="image_lg",
        ),
        migrations.RemoveField(
            model_name="projectitem",
            name="image_md",
        ),
        migrations.RemoveField(
            model_name="projectitem",
            name="image_sm",
        ),
    ]
