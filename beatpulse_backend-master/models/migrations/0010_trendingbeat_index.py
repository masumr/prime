# Generated by Django 2.1 on 2018-08-30 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_trendingbeat'),
    ]

    operations = [
        migrations.AddField(
            model_name='trendingbeat',
            name='index',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]