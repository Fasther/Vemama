# Generated by Django 3.0.4 on 2020-05-30 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0005_auto_20200509_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltask',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
