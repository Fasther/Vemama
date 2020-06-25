# Generated by Django 3.0.4 on 2020-05-09 21:59

import core.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [('core', '0001_initial'), ('core', '0002_auto_20200509_2251'), ('core', '0003_auto_20200509_2253'),
                ('core', '0004_auto_20200509_2256'), ('core', '0005_auto_20200509_2257'),
                ('core', '0006_auto_20200509_2259'), ('core', '0007_auto_20200509_2300'),
                ('core', '0008_profile_cities'), ('core', '0009_auto_20200509_2348')]

    initial = True

    dependencies = [
        ('cars', '0006_auto_20200503_1121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suitable_tasks', core.models.ChoiceArrayField(base_field=models.IntegerField(
                    choices=[(1, 'Regular cleaning and check'), (2, 'Big cleaning and check'),
                             (3, 'Service check / Oil change'), (4, 'STK'), (5, 'Tyres change'), (99, 'Other')]),
                                                                size=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile',
                                              to='core.Person', verbose_name='User')),
                ('cities', models.ManyToManyField(to='cars.City')),
            ],
        ),
    ]