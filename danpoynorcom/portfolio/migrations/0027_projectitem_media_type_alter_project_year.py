# Generated by Django 5.0 on 2024-01-08 22:09

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0026_fix_previous_migration_pngwebp_and_jpgwebp_extensions"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectitem",
            name="media_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="portfolio.mediatype",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="year",
            field=models.IntegerField(
                blank=True,
                help_text="Enter the project year as a 4-digit number",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1900),
                    django.core.validators.MaxValueValidator(2024),
                ],
            ),
        ),
    ]
