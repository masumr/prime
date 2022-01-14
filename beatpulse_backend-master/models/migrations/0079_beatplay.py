# Generated by Django 2.0.13 on 2019-04-12 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0078_auto_20190412_0732'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeatPlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.Beat')),
            ],
        ),
    ]