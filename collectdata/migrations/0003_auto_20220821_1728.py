# Generated by Django 3.2.13 on 2022-08-21 15:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('collectdata', '0002_auto_20220821_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basedata',
            name='user_file',
        ),
        migrations.AddField(
            model_name='basedata',
            name='base_file',
            field=models.FileField(default=django.utils.timezone.now, upload_to='mydocs/', verbose_name='base_file'),
            preserve_default=False,
        ),
    ]
