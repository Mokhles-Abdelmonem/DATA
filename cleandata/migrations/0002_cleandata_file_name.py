# Generated by Django 3.2.13 on 2022-08-21 16:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cleandata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleandata',
            name='file_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
