# Generated by Django 2.2.3 on 2019-08-20 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0111_auto_20190820_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpaypal',
            name='approved_order_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orderpaypal',
            name='paypal_order_id',
            field=models.CharField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]