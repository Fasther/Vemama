# Generated by Django 3.0.4 on 2020-04-22 20:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.IntegerField(choices=[(1, 'Regular cleaning and check'), (2, 'Big cleaning and check'),
                                               (3, 'Service check / Oil change'), (4, 'STK'), (5, 'Tires change'),
                                               (99, 'Other')], default=1),
        ),
    ]
