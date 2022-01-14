# Generated by Django 2.2 on 2019-04-29 07:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0090_remove_billinginfo_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beat',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=25), blank=True, help_text='tags to help with beat search', null=True, size=10),
        ),
    ]