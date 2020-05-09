# Generated by Django 3.0.4 on 2020-05-09 20:51

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='suitable_tasks',
            field=core.models.ChoiceArrayField(base_field=models.IntegerField(
                choices=[(1, 'Regular cleaning and check'), (2, 'Big cleaning and check'),
                         (3, 'Service check / Oil change'), (4, 'STK'), (5, 'Tyres change'), (99, 'Other')]),
                                               max_length=15, size=None),
        ),
    ]
