from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from allauth.socialaccount.models import SocialAccount
from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from amazons3_module.cloudfront import CLOUDFRONT_URL

PLATFORM_WEB = 'Web'
PLATFORM_ANDROID = 'Android'
PLATFORM_IOS = 'iOS'
PROFILE_PLATFORMS = (
    (PLATFORM_WEB, PLATFORM_WEB),
    (PLATFORM_ANDROID, PLATFORM_ANDROID),
    (PLATFORM_IOS, PLATFORM_IOS)
)

GROUP_ADMIN = 'Admin'
GROUP_UPLOADER = 'Uploader'
GROUP_PRODUCER = 'Producer'


class Profile(AbstractUser):
    # fields that are public to all apis
    public_fields = (
        'id', 'first_name', 'email', 'image_avatar_file_path', 'image_avatar_url', 'groups', 'date_of_creation')
    read_only_fields = ('id', 'email', 'groups', 'date_of_creation')
    
    email_subscription_active = models.BooleanField(default=True)
    platform = models.CharField(max_length=10, choices=PROFILE_PLATFORMS)
    date_of_creation = models.DateField(auto_now_add=True)
    image_avatar_file_path = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=55, blank=True)
    
    @property
    def image_avatar_url(self):
        return f'{CLOUDFRONT_URL}/{self.image_avatar_file_path}' if self.image_avatar_file_path else ''
    
    def is_social(self):
        return SocialAccount.objects.filter(user=self).exists()
    
    def add_email_address(self, request, new_email):
        # Add a new email address for the user, and send email confirmation.
        # Old email will remain the primary until the new one is confirmed.
        return EmailAddress.objects.add_email(request, self, new_email, confirm=True)
    
    def can_upload_in_dashboard(self):
        return self.groups.filter(name__in=[GROUP_ADMIN, GROUP_UPLOADER]).exists()
    
    def is_admin(self):
        return self.groups.filter(name__in=[GROUP_ADMIN]).exists()
    
    def __str__(self):
        return f'Profile {self.id} {self.email}'


@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # Once the email address is confirmed, make new email_address primary.
    # This also sets user.email to the new email address.
    # email_address is an instance of allauth.account.models.EmailAddress
    email_address.set_as_primary()
    # Get rid of old email addresses
    EmailAddress.objects.filter(
        user=email_address.user).exclude(primary=True).delete()


class BillingInfo(models.Model):
    public_fields = ('profile', 'full_name', 'email', 'street_address', 'city',
                     'zip_code', 'state', 'country')
    read_only_fields = ('profile',)
    
    profile = models.OneToOneField(Profile, primary_key=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    zip_code = models.CharField(max_length=25, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    country = models.CharField(max_length=25, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    @property
    def complete_address(self) -> str:
        address = ''
        if self.street_address:
            address += f'{self.street_address}, '
        if self.zip_code:
            address += f'{self.zip_code} '
        if self.city:
            address += f'{self.city} '
        if self.state:
            address += f'{self.state} '
        if self.country:
            address += self.country
        return address.strip()


@receiver(post_save, sender=Profile)
def create_billing_info(sender, instance: Profile, created, **kwargs):
    if created:
        BillingInfo.objects.create(profile=instance, full_name=instance.first_name, email=instance.email)


class AbstractLicenseOption(models.Model):
    """
    The license type choosen in the @CartItem
    """
    # fields that are public to all apis
    public_fields = ('id', 'name', 'price', 'color_hex', 'is_featured', 'has_mp3', 'has_wav', 'has_trackout',
                     'description_fields', 'description', 'detailed_license_url', 'contract_html')
    
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    price = models.FloatField()
    color_hex = models.CharField(max_length=10)
    is_featured = models.BooleanField(help_text='True if this licence will stand out')
    has_mp3 = models.BooleanField(help_text='True if the user will be able to get mp3')
    has_wav = models.BooleanField()
    has_trackout = models.BooleanField()
    detailed_license_url = models.URLField(null=True)
    contract_html = models.TextField(blank=True, max_length=15000)
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True


class LicenseOption(AbstractLicenseOption):
    pass


class LicenseOptionDescriptionField(models.Model):
    license_option = models.ForeignKey(LicenseOption, related_name='description_fields', on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    is_included = models.BooleanField()


class Producer(models.Model):
    # fields that are public to all apis
    public_fields = (
        'profile', 'display_name', 'bio', 'image_logo_url', 'image_background_url', 'contact_email',
        'number_of_followers', 'number_of_beats', 'is_featured', 'is_popular', 'slug')
    
    profile = models.OneToOneField(Profile, primary_key=True, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(db_index=True, unique=True, max_length=40)
    bio = models.TextField(max_length=500)
    image_logo_file_path = models.CharField(max_length=255)
    image_background_file_path = models.CharField(max_length=255)
    commission = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    paypal_email = models.CharField(max_length=50, null=True, blank=True)
    contact_email = models.CharField(max_length=50, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    # link that is shared between devices and that will open the app directly
    shareble_link = models.URLField(null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def get_total_sales(self):
        return OrderItemIncome.objects \
            .filter(order_item__order__status=Order.STATUS_COMPLETE, producer=self) \
            .aggregate(Sum('income'))['income__sum']
    
    @property
    def image_logo_url(self):
        return f'{CLOUDFRONT_URL}/{self.image_logo_file_path}'
    
    @property
    def image_background_url(self):
        return f'{CLOUDFRONT_URL}/{self.image_background_file_path}'
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name_plural = "Producers"


class AccountInvitation(models.Model):
    public_fields = '__all__'
    
    ROLES = (
        (GROUP_ADMIN, GROUP_ADMIN),
        (GROUP_UPLOADER, GROUP_UPLOADER),
        (GROUP_PRODUCER, GROUP_PRODUCER)
    )
    
    token = models.UUIDField(unique=True)
    # the role of the account invited
    role = models.CharField(max_length=10, choices=ROLES)
    # the email to which the token was sent
    email_sent_to = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)


class _AbstractBeatGroup(models.Model):
    # fields that are public to all apis
    public_fields = (
        'id', 'name', 'description', 'image_background_url', 'image_thumbnail_url', 'is_popular',
        'number_of_beats', 'beats', 'date_of_update')
    name = models.CharField(db_index=True, max_length=100, unique=True)
    slug = models.SlugField(db_index=True, unique=True, max_length=100)
    description = models.TextField(max_length=255, null=True, blank=True)
    image_thumbnail_file_path = models.CharField(max_length=500)
    image_background_file_path = models.CharField(max_length=500)
    order_position = models.FloatField(
        db_index=True, null=True, blank=True, help_text='The order in the list')
    date_of_update = models.DateTimeField(auto_now=True,
                                          help_text='this dates is updated when a new beat is added')
    is_popular = models.BooleanField()
    # link that is shared between devices and that will open the app directly
    shareble_link = models.URLField(null=True)
    
    @property
    def image_thumbnail_url(self):
        return f'{CLOUDFRONT_URL}/{self.image_thumbnail_file_path}'
    
    @property
    def image_background_url(self):
        return f'{CLOUDFRONT_URL}/{self.image_background_file_path}'
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True


class Genre(_AbstractBeatGroup):
    pass


class Mood(_AbstractBeatGroup):
    pass


class BeatKey(models.Model):
    # f#, Cmin
    name = models.CharField(db_index=True, max_length=25)


class Beat(models.Model):
    # fields that are public to all apis
    public_fields = (
        'id', 'name', 'genre', 'sub_genre', 'mood', 'image_url', 'image_thumbnail_url', 'bpm', 'key', 'sampled',
        'is_featured', 'producers', 'length', 'playlists', 'color_hex',
        'waveform_data', 'tags', 'date_of_release')
    
    name = models.CharField(db_index=True, max_length=100)
    producers = models.ManyToManyField(
        Producer, through='BeatProducerRelation')
    genre = models.ForeignKey(
        Genre, on_delete=models.PROTECT, related_name='beats', null=True)
    sub_genre = models.ForeignKey(
        Genre, on_delete=models.PROTECT, related_name='subgenre_beats', null=True)
    mood = models.ForeignKey(
        Mood, on_delete=models.PROTECT, related_name='beats', null=True)
    image_file_path = models.CharField(max_length=500, null=True)
    image_thumbnail_file_path = models.CharField(max_length=500,
                                                 help_text='A scalded version of the image. It should be 100x100',
                                                 null=True)
    tagged_file_path = models.CharField(max_length=255, blank=True, null=True)
    stream_file_path = models.CharField(max_length=255, blank=True, null=True,
                                        help_text='The ogg file used to stream the beat')
    mp3_file_path = models.CharField(max_length=255, blank=True, null=True)
    wav_file_path = models.CharField(max_length=255, blank=True, null=True)
    trackout_file_path = models.CharField(max_length=255, blank=True, null=True)
    trackout_external_url = models.URLField(max_length=255, blank=True, null=True)
    bpm = models.PositiveSmallIntegerField(null=True)
    key = models.ForeignKey(
        BeatKey, on_delete=models.PROTECT, help_text='For example F#, Cmin', null=True)
    length = models.PositiveSmallIntegerField(
        help_text='Length in seconds of the track', null=True)
    sampled = models.BooleanField()
    # demo_download_allowed = models.BooleanField()
    is_featured = models.BooleanField()
    date_of_release = models.DateField(
        null=True, blank=True, help_text='The date when the beat was published')
    # bought_exclusive_license = models.BooleanField(default=False)
    # exclusive_price = models.FloatField(null=True, blank=True, help_text='The price to buy this beat with exclusivity')
    color_hex = ColorField(
        help_text='the color represeting the beat. it is used as a shadow light in the app', null=True)
    waveform_data = ArrayField(models.FloatField(), null=True, blank=True, size=175,
                               help_text='the data points needed to create the audio wave form')
    tags = ArrayField(models.CharField(max_length=25), null=True, blank=True, size=10,
                      help_text='tags to help with beat search')
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(
        db_index=True, default=False, help_text='True if the beat does have all the files')
    shareble_link = models.URLField(null=True,
                                    help_text='link that is shared between devices and that will open the app directly')
    energy = models.PositiveSmallIntegerField(default=1, help_text='A number between 1 and 10')
    
    @property
    def image_thumbnail_url(self):
        return f'{CLOUDFRONT_URL}/{self.image_thumbnail_file_path}'
    
    @property
    def image_url(self):
        return f'{CLOUDFRONT_URL}/{self.image_file_path}'
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ('name',)


class BeatProducerRelation(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    commission = models.FloatField()


class TrendingBeat(models.Model):
    STATE_UP = 'Up'
    STATE_DOWN = 'Down'
    STATE_SAME = 'Same'
    STATE_NEW = 'New'
    STATES = (
        (STATE_UP, 'Went up'),
        (STATE_DOWN, 'Went down'),
        (STATE_SAME, 'Stayed the same'),
        (STATE_NEW, 'It is new'),
    )
    PERIOD_TODAY = 'Today'
    PERIOD_WEEK = 'Week'
    PERIOD_MONTH = 'Month'
    PERIOD_YEAR = 'Year'
    PERIOD_ALL_TIME = 'AllTime'
    PERIODS = (
        (PERIOD_TODAY, PERIOD_TODAY),
        (PERIOD_WEEK, 'This week'),
        (PERIOD_MONTH, 'This month'),
        (PERIOD_YEAR, 'This year'),
        (PERIOD_ALL_TIME, 'All time'),
    )
    index = models.PositiveSmallIntegerField()
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=10, choices=STATES, help_text='The state in the list')
    period = models.CharField(
        max_length=10, choices=PERIODS, help_text='The period')
    
    class Meta:
        unique_together = ('index', 'period')


class Playlist(_AbstractBeatGroup):
    # fields that are public to all apis
    public_fields = _AbstractBeatGroup.public_fields + \
                    ('is_featured_on_playlists', 'is_featured_on_browse', 'number_of_followers')
    
    is_featured_on_playlists = models.BooleanField()
    is_featured_on_browse = models.BooleanField()
    beats = models.ManyToManyField(Beat, related_name='playlists')
    date_of_creation = models.DateTimeField(
        auto_now_add=True, help_text='when it was first created')


class LikedBeat(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Checking for duplicate requests
        if LikedBeat.objects.filter(beat=self.beat, profile=self.profile).count() == 0:
            super().save(*args, **kwargs)


# class UserDownload(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
#
#
# class UserPlay(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     beat = models.ForeignKey(Beat, on_delete=models.CASCADE)


class Lyric(models.Model):
    public_fields = ('title', 'content')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    title = models.TextField(help_text='the lyric title')
    content = models.TextField(help_text='the content of the lyric')
    
    def save(self, *args, **kwargs):
        # Checking for duplicate requests
        if Lyric.objects.filter(beat=self.beat, profile=self.profile).count() == 0:
            super().save(*args, **kwargs)


class FollowedProducer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Checking for duplicate requests
        if FollowedProducer.objects.filter(producer=self.producer, profile=self.profile).count() == 0:
            super().save(*args, **kwargs)


class FollowedPlaylist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Checking for duplicate requests
        if FollowedPlaylist.objects.filter(playlist=self.playlist, profile=self.profile).count() == 0:
            super().save(*args, **kwargs)


class Coupon(models.Model):
    public_fields = ('id', 'token', 'discount_percentage',
                     'licenses', 'expiration_date')
    token = models.CharField(max_length=255, unique=True,
                             help_text='The actual code of the coupon')
    discount_percentage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                              help_text='The percentage of discount')
    licenses = models.ManyToManyField(LicenseOption, help_text='The licenses that are discounted')
    expiration_date = models.DateField(null=True, blank=True, help_text='The expiration date of the coupon')
    
    def __str__(self):
        return self.token


class Deal(models.Model):
    public_fields = ('id', 'buy', 'get', 'excluded_licenses')
    buy = models.PositiveSmallIntegerField(help_text='Minimum number of tracks in cart')
    get = models.PositiveSmallIntegerField(help_text='Number of free tracks')
    excluded_licenses = models.ManyToManyField(LicenseOption, help_text='The licenses that are exluded from the deal')
    
    def needed_beats(self):
        return self.buy + self.get
    
    def __str__(self):
        return f'Buy {self.buy} Get {self.buy}'


# Orders & Payments

class CartItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    license_option = models.ForeignKey(LicenseOption, on_delete=models.CASCADE)
    added_on_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('profile', 'beat',)


class LicenseBought(AbstractLicenseOption):
    price_discounted = models.FloatField(
        help_text='The price paid for the license after deals and coupons')


class Order(models.Model):
    """
    Each one represents an order a user made
    """
    STATUS_PENDING = 'Pending'
    STATUS_COMPLETE = 'Complete'
    STATUS_REVERSE = 'Reverse'
    STATUS_REFUNDED = 'Refunded'
    STATUSES = (
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_COMPLETE, STATUS_COMPLETE),
        (STATUS_REVERSE, STATUS_REVERSE),
        (STATUS_REFUNDED, STATUS_REFUNDED),
    )
    
    PAYMENT_PLATFORM_CREDIT_CARD = 'Credit Card'
    PAYMENT_PLATFORM_PAYPAL = 'PayPal'
    PAYMENT_PLATFORM_ALIPAY = 'Alipay'
    PAYMENT_PLATFORMS = (
        (PAYMENT_PLATFORM_CREDIT_CARD, PAYMENT_PLATFORM_CREDIT_CARD),
        (PAYMENT_PLATFORM_PAYPAL, PAYMENT_PLATFORM_PAYPAL),
        (PAYMENT_PLATFORM_ALIPAY, PAYMENT_PLATFORM_ALIPAY)
    )
    
    public_fields = (
        'id', 'date', 'profile_platform', 'status', 'payment_platform', 'total', 'items',
        'profile_address', 'profile_email', 'total_discount', 'profile_ip', 'payment_provider_charge_id')
    public_fields_admin = public_fields + ('profile', 'quantity', 'producer_cut')
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUSES, default=STATUS_PENDING)
    date = models.DateTimeField(auto_now_add=True)
    profile_ip = models.CharField(max_length=45, help_text='The IP of the customer when he made the payment')
    profile_address = models.CharField(max_length=255)
    profile_platform = models.CharField(max_length=10, choices=PROFILE_PLATFORMS)
    profile_email = models.EmailField()
    payment_platform = models.CharField(max_length=25, choices=PAYMENT_PLATFORMS)
    total = models.FloatField(help_text='The total price the client paid after coupons and deals')
    
    def __str__(self):
        return f'{self.id} {self.profile.id} {self.date}'
    
    @property
    def total_discount(self):
        total_without_discounts = OrderItem.objects.filter(order=self) \
            .aggregate(Sum('license__price'))['license__price__sum']
        return total_without_discounts - self.total


class OrderStripe(models.Model):
    order = models.OneToOneField(Order, primary_key=True, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True, null=True)
    charge_id = models.CharField(max_length=100, unique=True, null=True)
    source_id = models.CharField(max_length=100, unique=True, null=True)


class OrderPaypal(models.Model):
    order = models.OneToOneField(Order, primary_key=True, on_delete=models.CASCADE)
    paypal_order_id = models.CharField(max_length=100, unique=True)
    payment_capture_id = models.CharField(max_length=100, null=True)
    # approved_order_id = models.CharField(max_length=100, null=True)
    json_result = JSONField()


class OrderItem(models.Model):
    public_fields = ('id', 'beat', 'license', 'downloads')
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.PROTECT)
    license = models.OneToOneField(LicenseBought, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)
        
        from analytics_module.models import BeatPopularityIncrease
        BeatPopularityIncrease.objects.create(beat=self.beat,
                                              increase_amount=BeatPopularityIncrease.AMOUNT_FOR_SALE)
    
    def delete(self, *args, **kwargs):
        self.license.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class OrderItemIncome(models.Model):
    public_fields = ('producer', 'income')
    
    order_item = models.ForeignKey(OrderItem, related_name='producer_incomes', on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    income = models.FloatField()


class OrderItemDownload(models.Model):
    public_fields = ('profile', 'date', 'profile_ip')
    
    order_item = models.ForeignKey(OrderItem, related_name='downloads', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    profile_ip = models.CharField(
        max_length=45, help_text='The IP of the customer when he made the download')


class ProducerPayout(models.Model):
    """
    Each one represents a payment to the producer
    """
    public_fields = ('id', 'producer', 'date', 'payed_amount', 'description_fields', 'beats_sold')
    
    producer = models.ForeignKey(Producer, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    payed_amount = models.FloatField()


class ProducerPayoutDescriptionField(models.Model):
    producer_payout = models.ForeignKey(ProducerPayout, related_name='description_fields', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.FloatField()
