# Generated by Django 3.2.9 on 2022-02-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_alter_vacations_line_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='loglist',
            name='full_name',
            field=models.CharField(default='-', max_length=250, verbose_name='Компания'),
        ),
        migrations.AddField(
            model_name='vacations',
            name='full_name',
            field=models.CharField(default='-', max_length=250, verbose_name='Компания'),
        ),
    ]
