# Generated by Django 2.0.8 on 2018-09-06 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0010_trendingbeat_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='trendingbeat',
            name='state',
            field=models.CharField(choices=[('Up', 'Went up'), ('Down', 'Went down'), ('Same', 'Stayed the same'), ('New', 'It is new')], default='New', help_text='The state in the list', max_length=10),
            preserve_default=False,
        ),
    ]
