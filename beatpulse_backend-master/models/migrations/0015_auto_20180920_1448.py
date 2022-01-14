# Generated by Django 2.1.1 on 2018-09-20 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0014_producer_is_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy', models.PositiveSmallIntegerField(help_text='Minimum number of tracks in cart')),
                ('get', models.PositiveSmallIntegerField(help_text='Number of free tracks')),
                ('excluded_licenses', models.ManyToManyField(help_text='The licenses that are exluded from the deal', to='models.LicenseOption')),
            ],
        ),
        migrations.AlterField(
            model_name='beat',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='beats', to='models.Genre'),
        ),
        migrations.AlterField(
            model_name='beat',
            name='mood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='beats', to='models.Mood'),
        ),
        migrations.AlterField(
            model_name='beat',
            name='sub_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subgenre_beats', to='models.Genre'),
        ),
    ]
