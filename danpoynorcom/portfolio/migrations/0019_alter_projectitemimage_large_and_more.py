# Generated by Django 5.0 on 2023-12-21 22:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0018_alter_projectitemattachment_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectitemimage",
            name="large",
            field=models.URLField(
                blank=True,
                null=True,
                validators=[django.core.validators.URLValidator()],
            ),
        ),
        migrations.AlterField(
            model_name="projectitemimage",
            name="medium_large",
            field=models.URLField(
                blank=True,
                null=True,
                validators=[django.core.validators.URLValidator()],
            ),
        ),
    ]
