# Generated by Django 2.1.7 on 2019-04-12 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0079_beatplay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beatplay',
            name='beat',
        ),
        migrations.DeleteModel(
            name='BeatPlay',
        ),
    ]
