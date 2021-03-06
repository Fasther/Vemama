# Generated by Django 3.0.7 on 2020-10-29 19:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0009_auto_20200926_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='car_service_days_threshold',
            field=models.IntegerField(default=30, help_text='How many DAYs before task for service will popup',
                                      verbose_name='Days service threshold'),
        ),
        migrations.AddField(
            model_name='city',
            name='car_service_km_threshold',
            field=models.IntegerField(default=3000, help_text='How many KMs before task for service will popup',
                                      verbose_name='KMs service threshold'),
        ),
        migrations.AddField(
            model_name='city',
            name='car_tyre_switch_days_threshold',
            field=models.IntegerField(default=45, help_text='How many days before tyres switch date',
                                      verbose_name='Tyre switch days delay'),
        ),
    ]
