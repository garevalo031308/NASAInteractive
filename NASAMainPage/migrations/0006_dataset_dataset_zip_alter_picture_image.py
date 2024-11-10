# Generated by Django 5.1.2 on 2024-11-10 19:38

import NASAMainPage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "NASAMainPage",
            "0005_aimodel_model_dataset_alter_aimodel_model_path_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="dataset_zip",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="temp/",
                validators=[NASAMainPage.models.validate_zip_file],
            ),
        ),
        migrations.AlterField(
            model_name="picture",
            name="image",
            field=models.ImageField(
                upload_to="temp/",
                validators=[NASAMainPage.models.validate_picture_file],
            ),
        ),
    ]
