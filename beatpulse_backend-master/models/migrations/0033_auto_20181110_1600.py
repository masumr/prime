# Generated by Django 2.1.3 on 2018-11-10 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0032_auto_20181109_1716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beat',
            old_name='mp3_file_name',
            new_name='mp3_file_path',
        ),
        migrations.RenameField(
            model_name='beat',
            old_name='tagged_file_name',
            new_name='tagged_file_path',
        ),
        migrations.RenameField(
            model_name='beat',
            old_name='trackout_file_name',
            new_name='trackout_file_path',
        ),
        migrations.RenameField(
            model_name='beat',
            old_name='wav_file_name',
            new_name='wav_file_path',
        ),
    ]
