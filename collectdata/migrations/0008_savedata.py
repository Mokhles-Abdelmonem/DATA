# Generated by Django 3.2.13 on 2022-09-02 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collectdata', '0007_basedata_refine_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save', models.TextField(blank=True, null=True)),
                ('data_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collectdata.basedata')),
            ],
        ),
    ]
