# Generated by Django 2.2.3 on 2019-08-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0109_auto_20190820_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpaypal',
            name='approved_order_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='orderpaypal',
            name='paypal_payment_capture_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
