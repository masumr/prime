# Generated by Django 2.0.10 on 2019-03-12 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0063_auto_20190312_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='image_background_url',
            new_name='image_background_file_path',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='image_thumbnail_url',
            new_name='image_thumbnail_file_path',
        ),
        migrations.RenameField(
            model_name='mood',
            old_name='image_background_url',
            new_name='image_background_file_path',
        ),
        migrations.RenameField(
            model_name='mood',
            old_name='image_thumbnail_url',
            new_name='image_thumbnail_file_path',
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='image_background_url',
            new_name='image_background_file_path',
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='image_thumbnail_url',
            new_name='image_thumbnail_file_path',
        ),
    ]
