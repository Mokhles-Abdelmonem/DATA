# Generated by Django 3.2.13 on 2022-09-02 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collectdata', '0011_rename_saved_savedata_saved_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basedata',
            name='refine_file',
        ),
    ]
