# Generated by Django 2.1.1 on 2018-10-02 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0023_auto_20180925_1714'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPlay',
            new_name='LikedBeat',
        ),
        migrations.RemoveField(
            model_name='userdownload',
            name='beat',
        ),
        migrations.RemoveField(
            model_name='userdownload',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='userfavorite',
            name='beat',
        ),
        migrations.RemoveField(
            model_name='userfavorite',
            name='profile',
        ),
        migrations.AlterUniqueTogether(
            name='likedbeat',
            unique_together={('profile', 'beat')},
        ),
        migrations.DeleteModel(
            name='UserDownload',
        ),
        migrations.DeleteModel(
            name='UserFavorite',
        ),
    ]