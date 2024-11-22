# Generated by Django 5.1.2 on 2024-11-21 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NASAMainPage', '0008_usercustomsections_remove_fold_excel_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fold',
            name='accuracy',
        ),
        migrations.RemoveField(
            model_name='fold',
            name='confusion_matrix',
        ),
        migrations.RemoveField(
            model_name='fold',
            name='fold_number',
        ),
        migrations.CreateModel(
            name='FoldInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fold_number', models.IntegerField()),
                ('confusion_matrix', models.ImageField(upload_to='')),
                ('fold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.fold')),
            ],
        ),
        migrations.CreateModel(
            name='FoldClassInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precision', models.IntegerField()),
                ('recall', models.IntegerField()),
                ('f1score', models.IntegerField()),
                ('support', models.IntegerField()),
                ('accuracy', models.IntegerField()),
                ('dataset_class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.datasetclasses')),
                ('foldinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NASAMainPage.foldinfo')),
            ],
        ),
        migrations.DeleteModel(
            name='ClassInfo',
        ),
    ]
