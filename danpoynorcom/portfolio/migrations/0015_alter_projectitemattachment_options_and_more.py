# Generated by Django 5.0 on 2023-12-21 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0014_projectitemattachment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="projectitemattachment",
            options={
                "verbose_name": "Project Attachment",
                "verbose_name_plural": "Project Attachments",
            },
        ),
        migrations.AlterField(
            model_name="projectitemattachment",
            name="file",
            field=models.FileField(upload_to="portfolio_attachments/"),
        ),
        migrations.AlterModelTable(
            name="projectitemattachment",
            table="portfolio_project_item_attachment",
        ),
    ]
