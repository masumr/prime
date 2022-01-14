# Generated by Django 2.2.2 on 2019-06-30 15:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0106_producer_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beat',
            name='waveform_data',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, help_text='the data points needed to create the audio wave form', null=True, size=175),
        ),
    ]