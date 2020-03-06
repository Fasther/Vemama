# Generated by Django 2.2.3 on 2019-08-21 12:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_actual_driven_kms',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
