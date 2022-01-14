# Generated by Django 2.1 on 2018-08-30 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_auto_20180830_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendingBeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_today', models.BooleanField(default=False)),
                ('is_week', models.BooleanField(default=False)),
                ('is_month', models.BooleanField(default=False)),
                ('is_year', models.BooleanField(default=False)),
                ('is_all_time', models.BooleanField(default=False)),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Beat')),
            ],
        ),
    ]