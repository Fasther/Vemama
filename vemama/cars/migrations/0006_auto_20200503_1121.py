# Generated by Django 3.0.4 on 2020-05-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0005_historicalcar'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_next_date',
            field=models.DateField(blank=True, null=True, verbose_name='Next 🔧 date'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_next_km',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True,
                                      verbose_name='Next 🔧 kms'),
        ),
        migrations.AddField(
            model_name='historicalcar',
            name='car_next_date',
            field=models.DateField(blank=True, null=True, verbose_name='Next 🔧 date'),
        ),
        migrations.AddField(
            model_name='historicalcar',
            name='car_next_km',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True,
                                      verbose_name='Next 🔧 kms'),
        ),
    ]
