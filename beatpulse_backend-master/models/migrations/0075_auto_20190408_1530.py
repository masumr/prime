# Generated by Django 2.1.7 on 2019-04-08 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0074_auto_20190406_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image_avatar_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='image_avatar_file_path',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]