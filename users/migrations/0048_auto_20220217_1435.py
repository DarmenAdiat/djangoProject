# Generated by Django 3.2.9 on 2022-02-17 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0047_auto_20220209_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='loglist',
            name='decree',
            field=models.CharField(default='', max_length=250, null=True, verbose_name='Приказ'),
        ),
        migrations.AddField(
            model_name='vacations',
            name='decree',
            field=models.CharField(default='', max_length=250, null=True, verbose_name='Приказ'),
        ),
        migrations.AddField(
            model_name='vacations',
            name='description',
            field=models.CharField(default='', max_length=250, null=True, verbose_name='Описание/Номер'),
        ),
    ]