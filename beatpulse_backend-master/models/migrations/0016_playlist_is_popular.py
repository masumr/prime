# Generated by Django 2.1.1 on 2018-09-21 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0015_auto_20180920_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='is_popular',
            field=models.BooleanField(default=False),
        ),
    ]