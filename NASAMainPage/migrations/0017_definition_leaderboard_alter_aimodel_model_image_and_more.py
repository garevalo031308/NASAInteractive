# Generated by Django 5.0.6 on 2025-04-02 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NASAMainPage', '0016_alter_aimodel_model_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=200)),
                ('definition', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('score', models.FloatField()),
                ('game_mode', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='aimodel',
            name='model_image',
            field=models.ImageField(upload_to='NASAMainPage/static/images/models/<django.db.models.fields.CharField>'),
        ),
        migrations.AlterField(
            model_name='fold',
            name='fold_name',
            field=models.CharField(editable=False, max_length=200),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gamemode', models.CharField(max_length=200)),
                ('difficulty', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('total_score', models.IntegerField()),
                ('number_of_rounds', models.IntegerField()),
                ('number_correct', models.IntegerField()),
                ('number_incorrect', models.IntegerField()),
                ('active_game', models.BooleanField()),
                ('ai_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.aimodel')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField()),
                ('score', models.IntegerField()),
                ('correct', models.BooleanField()),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.game')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.picture')),
            ],
        ),
        migrations.CreateModel(
            name='Scoreboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('score', models.FloatField()),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.game')),
            ],
        ),
    ]
