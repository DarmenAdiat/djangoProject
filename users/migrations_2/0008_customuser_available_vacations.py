# Generated by Django 3.2.9 on 2021-11-11 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_loglist_id_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='available_vacations',
            field=models.IntegerField(blank=True, default=0, max_length=3, verbose_name='Доступные дни отпуска'),
        ),
    ]