# Generated by Django 5.0.6 on 2025-04-02 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NASAMainPage', '0018_round_image_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='image_class',
        ),
    ]
