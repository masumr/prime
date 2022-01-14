# Generated by Django 2.0.9 on 2018-11-01 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0027_beat_exclusive_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lyric',
            name='lyric',
        ),
        migrations.AddField(
            model_name='lyric',
            name='content',
            field=models.TextField(default='', help_text='the content of the lyric'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lyric',
            name='title',
            field=models.TextField(default='', help_text='the lyric title'),
            preserve_default=False,
        ),
    ]