# Generated by Django 2.1.3 on 2018-11-30 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0038_auto_20181130_1008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beat',
            old_name='key_2',
            new_name='key',
        ),
    ]
