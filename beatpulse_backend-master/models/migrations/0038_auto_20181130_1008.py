# Generated by Django 2.1.3 on 2018-11-30 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0037_auto_20181130_0929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beat',
            name='key',
        ),
        migrations.AddField(
            model_name='beat',
            name='key_2',
            field=models.ForeignKey(default=1, help_text='For example F#, Cmin', on_delete=django.db.models.deletion.PROTECT, to='models.BeatKey'),
            preserve_default=False,
        ),
    ]
