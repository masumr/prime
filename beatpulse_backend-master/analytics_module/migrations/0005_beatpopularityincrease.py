# Generated by Django 2.0.13 on 2019-04-17 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0084_auto_20190417_0850'),
        ('analytics_module', '0004_auto_20190417_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeatPopularityIncrease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('increase_amount', models.PositiveSmallIntegerField()),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Beat')),
            ],
        ),
    ]
