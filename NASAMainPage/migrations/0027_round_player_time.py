# Generated by Django 5.0.6 on 2025-04-07 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NASAMainPage', '0026_round_ai_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='player_time',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
