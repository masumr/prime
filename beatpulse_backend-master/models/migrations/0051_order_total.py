# Generated by Django 2.0.10 on 2019-02-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0050_auto_20190207_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]