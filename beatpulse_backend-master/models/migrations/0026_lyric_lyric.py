# Generated by Django 2.0.9 on 2018-10-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0025_auto_20181005_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='lyric',
            name='lyric',
            field=models.TextField(default='', help_text='the lyric'),
            preserve_default=False,
        ),
    ]