# Generated by Django 2.1.1 on 2018-09-25 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0021_auto_20180925_1706'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trendingbeat',
            unique_together={('index', 'period')},
        ),
    ]
