# Generated by Django 5.1.2 on 2024-11-11 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("NASAMainPage", "0002_alter_dataset_dataset_number_of_images"),
    ]

    operations = [
        migrations.DeleteModel(
            name="InsertDatasetZip",
        ),
    ]
