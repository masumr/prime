# Generated by Django 2.1 on 2018-08-24 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_auto_20180824_0910'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beat',
            old_name='producer',
            new_name='producers',
        ),
        migrations.AlterField(
            model_name='licenseoptiondescriptionfield',
            name='license_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='description_fields', to='models.LicenseOption'),
        ),
    ]
