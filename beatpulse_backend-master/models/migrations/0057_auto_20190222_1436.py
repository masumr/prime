# Generated by Django 2.0.10 on 2019-02-22 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0056_accountinvitation_full_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountinvitation',
            old_name='full_name',
            new_name='name',
        ),
    ]