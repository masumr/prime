# Generated by Django 2.1 on 2018-08-23 13:38

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('total_spent', models.FloatField(default=0)),
                ('stripe_id', models.CharField(blank=True, max_length=255, null=True)),
                ('email_subscription_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ArtistType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('image_thumbnail_url', models.URLField(blank=True, max_length=500, null=True)),
                ('image_background_url', models.URLField(blank=True, max_length=500, null=True)),
                ('order_position', models.FloatField(db_index=True, help_text='The order in the list', null=True)),
                ('is_featured_on_browse', models.BooleanField(default=False)),
                ('is_featured_on_playlists', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Beat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('image_url', models.CharField(blank=True, max_length=500)),
                ('tagged_file_name', models.CharField(blank=True, max_length=255)),
                ('mp3_file_name', models.CharField(blank=True, max_length=255)),
                ('wav_file_name', models.CharField(blank=True, max_length=255)),
                ('trackout_file_name', models.CharField(blank=True, max_length=255)),
                ('bpm', models.PositiveSmallIntegerField()),
                ('key', models.CharField(blank=True, max_length=5)),
                ('length', models.PositiveSmallIntegerField(help_text='Length in seconds of the track')),
                ('sampled', models.BooleanField()),
                ('demo_download_allowed', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('published', models.BooleanField(db_index=True, default=False, help_text='True if the beat does have all the files')),
                ('date_of_publishing', models.DateField(blank=True, help_text='The date when the beat was published', null=True)),
                ('bought_exlusive_license', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='BundleDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deal_buy', models.IntegerField(default=1)),
                ('deal_get', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(help_text='The actual code of the coupon', max_length=255)),
                ('discount_percentage', models.IntegerField(help_text='The percentage of discount', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('expiration_date', models.DateField(help_text='The expiration date of the coupon', null=True)),
                ('is_never_expiring', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FollowedPlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FollowedProducer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('image_thumbnail_url', models.URLField(blank=True, max_length=500, null=True)),
                ('image_background_url', models.URLField(blank=True, max_length=500, null=True)),
                ('order_position', models.FloatField(db_index=True, help_text='The order in the list', null=True)),
                ('is_featured_on_browse', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LicenseOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField(null=True)),
                ('color_hex', models.CharField(max_length=10)),
                ('is_featured', models.BooleanField(default=False, help_text='True if this licence will stand out')),
                ('has_mp3', models.BooleanField(default=True, help_text='True if the user will be able to get mp3')),
                ('has_wav', models.BooleanField()),
                ('has_trackout', models.BooleanField()),
                ('contract_html', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lyric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Beat')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('image_thumbnail_url', models.URLField(blank=True, max_length=500, null=True)),
                ('image_background_url', models.URLField(blank=True, max_length=500, null=True)),
                ('order_position', models.FloatField(db_index=True, help_text='The order in the list', null=True)),
                ('is_featured_on_browse', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('image_thumbnail_url', models.URLField(blank=True, max_length=500, null=True)),
                ('image_background_url', models.URLField(blank=True, max_length=500, null=True)),
                ('order_position', models.FloatField(db_index=True, help_text='The order in the list', null=True)),
                ('is_featured_on_browse', models.BooleanField(default=False)),
                ('is_featured_on_playlists', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('image_logo_url', models.CharField(max_length=255, null=True)),
                ('image_background_url', models.CharField(blank=True, max_length=255, null=True)),
                ('commission', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('paypal_email', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=50, null=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Producers',
            },
        ),
        migrations.CreateModel(
            name='ProducerPayout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payed_amount', models.FloatField()),
                ('payed_on_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Producer')),
            ],
        ),
        migrations.CreateModel(
            name='UserDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Beat')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Beat')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Beat')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='followedproducer',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Producer'),
        ),
        migrations.AddField(
            model_name='followedproducer',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='followedplaylist',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Playlist'),
        ),
        migrations.AddField(
            model_name='followedplaylist',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coupon',
            name='licenses',
            field=models.ManyToManyField(help_text='The licenses that are discounted', to='models.LicenseOption'),
        ),
        migrations.AddField(
            model_name='bundledeal',
            name='licenses',
            field=models.ManyToManyField(to='models.LicenseOption'),
        ),
        migrations.AddField(
            model_name='beat',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='genre', to='models.Genre'),
        ),
        migrations.AddField(
            model_name='beat',
            name='producer',
            field=models.ManyToManyField(to='models.Producer'),
        ),
        migrations.AddField(
            model_name='beat',
            name='sub_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sub_genre', to='models.Genre'),
        ),
        migrations.AlterUniqueTogether(
            name='followedproducer',
            unique_together={('profile', 'producer')},
        ),
        migrations.AlterUniqueTogether(
            name='followedplaylist',
            unique_together={('profile', 'playlist')},
        ),
    ]