# Generated by Django 3.2.9 on 2022-03-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0049_editemails_editphone'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaySlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Payslips',
                'verbose_name_plural': 'Payslips',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='profile_images', verbose_name='Аватарка'),
        ),
    ]
