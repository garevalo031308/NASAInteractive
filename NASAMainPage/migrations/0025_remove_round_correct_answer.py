# Generated by Django 5.0.6 on 2025-04-07 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NASAMainPage', '0024_round_correct_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='correct_answer',
        ),
    ]
