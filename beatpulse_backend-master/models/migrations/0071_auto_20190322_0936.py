# Generated by Django 2.0.13 on 2019-03-22 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0070_auto_20190322_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountinvitation',
            name='email_sent_to',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]