# Generated by Django 3.2.9 on 2021-11-10 11:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20211110_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loglist',
            name='id_user',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Идентификатор пользователя'),
        ),
    ]