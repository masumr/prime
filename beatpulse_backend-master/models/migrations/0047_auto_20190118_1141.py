# Generated by Django 2.0.10 on 2019-01-18 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0046_auto_20190118_1103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billinginfo',
            name='id',
        ),
        migrations.RemoveField(
            model_name='producer',
            name='id',
        ),
        migrations.AlterField(
            model_name='billinginfo',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='producer',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
