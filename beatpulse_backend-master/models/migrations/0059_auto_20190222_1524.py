# Generated by Django 2.0.10 on 2019-02-22 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0058_auto_20190222_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountinvitation',
            name='email_sent_to',
            field=models.EmailField(max_length=255),
        ),
    ]
