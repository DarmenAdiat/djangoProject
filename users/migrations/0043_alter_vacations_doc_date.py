# Generated by Django 3.2.9 on 2022-02-02 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_alter_loglist_doc_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacations',
            name='doc_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата создания'),
        ),
    ]