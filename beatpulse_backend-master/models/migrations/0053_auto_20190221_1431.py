# Generated by Django 2.0.10 on 2019-02-21 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0052_auto_20190219_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='profile_ip',
            field=models.CharField(help_text='The IP of the customer when he made the payment', max_length=45),
        ),
    ]