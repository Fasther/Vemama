# Generated by Django 3.0.4 on 2020-04-22 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0004_auto_20200422_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCar',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Use to deactivate car. Deactivated cars do not get automatic tasks and reminders.',
                                                  verbose_name='Active')),
                ('car_name', models.CharField(db_index=True, max_length=200, verbose_name='Name')),
                ('car_id', models.DecimalField(db_index=True, decimal_places=0,
                                               help_text='ID for finding car in Zemtu, Convadis,...', max_digits=5,
                                               verbose_name='External ID')),
                ('car_tyres',
                 models.IntegerField(blank=True, choices=[(1, 'All year'), (2, 'Summer'), (3, 'Winter')], default=1,
                                     help_text='If seasonal tyre change is needed, task will be planned', null=True,
                                     verbose_name='Actual Tyres')),
                ('car_dirtiness', models.IntegerField(blank=True, choices=[(1, 'Fine, looks good'),
                                                                           (2, 'Few stains, still good enough'),
                                                                           (3, 'Car needs wet cleaning. Really.')],
                                                      default=1, help_text='Applies just for big/wet cleaning.',
                                                      null=True, verbose_name='Need of wet cleaning')),
                ('car_next_inspection_date', models.DateField(verbose_name='Next inspection date')),
                ('car_next_inspection_km',
                 models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Next inspection KMs')),
                ('car_next_oil_date', models.DateField(verbose_name='Next oil change date')),
                ('car_next_oil_km',
                 models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Next oil change KMs')),
                ('car_next_stk_date', models.DateField(blank=True, null=True, verbose_name='Next STK date')),
                ('car_last_check', models.DateField(blank=True, null=True, verbose_name='Last check')),
                ('car_actual_driven_kms',
                 models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Driven KMs')),
                ('car_note', models.TextField(blank=True, max_length=1024, verbose_name='Notes')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('car_city', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                               on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                               to='cars.City', verbose_name='City')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical car',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]