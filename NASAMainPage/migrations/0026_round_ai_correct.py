# Generated by Django 5.0.6 on 2025-04-07 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NASAMainPage', '0025_remove_round_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='ai_correct',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
