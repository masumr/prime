# Generated by Django 2.1.1 on 2018-09-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0011_trendingbeat_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trendingbeat',
            name='is_all_time',
        ),
        migrations.RemoveField(
            model_name='trendingbeat',
            name='is_month',
        ),
        migrations.RemoveField(
            model_name='trendingbeat',
            name='is_today',
        ),
        migrations.RemoveField(
            model_name='trendingbeat',
            name='is_week',
        ),
        migrations.RemoveField(
            model_name='trendingbeat',
            name='is_year',
        ),
        migrations.AddField(
            model_name='trendingbeat',
            name='period',
            field=models.CharField(choices=[('Today', 'Today'), ('Week', 'This week'), ('Month', 'This month'), ('Year', 'This year'), ('All time', 'All time')], default='Today', help_text='The period', max_length=10),
            preserve_default=False,
        ),
    ]
