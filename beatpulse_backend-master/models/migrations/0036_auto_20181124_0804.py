# Generated by Django 2.1.3 on 2018-11-24 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0035_auto_20181124_0804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beat',
            old_name='producers_new',
            new_name='producers',
        ),
    ]