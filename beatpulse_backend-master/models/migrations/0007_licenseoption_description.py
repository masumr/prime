# Generated by Django 2.1 on 2018-08-26 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_auto_20180825_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='licenseoption',
            name='description',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
