# Generated by Django 2.1.3 on 2018-11-06 13:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0028_auto_20181101_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='date_of_creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='profile',
            name='platform',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
