# Generated by Django 3.2.13 on 2022-09-02 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collectdata', '0009_savedata_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savedata',
            old_name='save',
            new_name='saved',
        ),
    ]
