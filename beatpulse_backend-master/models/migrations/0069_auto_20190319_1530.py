# Generated by Django 2.0.13 on 2019-03-19 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0068_auto_20190315_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountinvitation',
            name='email_sent_to',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
