# Generated by Django 3.0.4 on 2020-05-03 19:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0003_historicaltask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltask',
            name='task_type',
            field=models.IntegerField(choices=[(1, 'Regular cleaning and check'), (2, 'Big cleaning and check'),
                                               (3, 'Service check / Oil change'), (4, 'STK'), (5, 'Tyres change'),
                                               (99, 'Other')], default=1),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.IntegerField(choices=[(1, 'Regular cleaning and check'), (2, 'Big cleaning and check'),
                                               (3, 'Service check / Oil change'), (4, 'STK'), (5, 'Tyres change'),
                                               (99, 'Other')], default=1),
        ),
    ]
