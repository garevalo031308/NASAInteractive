# Generated by Django 5.1.2 on 2024-11-22 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NASAMainPage', '0014_alter_foldinfo_confusion_matrix_usersections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersections',
            name='section_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
