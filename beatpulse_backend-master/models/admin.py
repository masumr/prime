from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, LicenseOption, Playlist, Mood, Genre, Beat, Producer, LicenseOptionDescriptionField, \
    TrendingBeat, Coupon, Deal, FollowedProducer, FollowedPlaylist, LikedBeat, BeatProducerRelation, Lyric, BeatKey, \
    ProducerPayout, Order, OrderItem, ProducerPayoutDescriptionField, LicenseBought, OrderItemIncome, BillingInfo, \
    OrderItemDownload, AccountInvitation, OrderStripe, OrderPaypal


class BeatProducerRelationInline(admin.TabularInline):
    model = BeatProducerRelation
    extra = 1


class BeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','date_of_release')
    search_fields = ['name','producers__display_name' ]
    inlines = (BeatProducerRelationInline,)


class LicenseOptionDescriptionFieldInline(admin.TabularInline):
    model = LicenseOptionDescriptionField
    extra = 1


class LicenseOptionAdmin(admin.ModelAdmin):
    inlines = [LicenseOptionDescriptionFieldInline]
    list_display = ('id', 'name')
    search_fields = ['name', ]


class LicenseBoughtAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'price_discounted')


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'display_name')
    search_fields = ['display_name', ]


class BillingInfoInline(admin.TabularInline):
    model = BillingInfo


class ProfileAdmin(UserAdmin):
    inlines = [BillingInfoInline]
    # column names
    list_display = ('email', 'first_name', 'last_name', 'verified')
    # fields that can be looked for when searching
    search_fields = ['email']
    
    @staticmethod
    def verified(obj: Profile):
        return EmailAddress.objects.filter(user=obj, verified=True).exists()


class _AbstractBeatGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name', ]


class PlaylistAdmin(_AbstractBeatGroupAdmin):
    pass


class GenreAdmin(_AbstractBeatGroupAdmin):
    pass


class MoodAdmin(_AbstractBeatGroupAdmin):
    pass


class TrendingBeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'state')


class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'discount_percentage', 'expiration_date')


class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'buy', 'get')


class FollowedProducerAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'producer')


class FollowedPlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'playlist')


class LikedBeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'beat')


class LyricAdmin(admin.ModelAdmin):
    list_display = ('profile', 'beat', 'title', 'content')


class BeatKeyAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProducerPayoutDescriptionFieldInline(admin.TabularInline):
    model = ProducerPayoutDescriptionField
    extra = 1


class ProducerPayoutAdmin(admin.ModelAdmin):
    inlines = [ProducerPayoutDescriptionFieldInline]
    list_display = ('id', 'producer', 'date', 'payed_amount')


class OrderItemDownloadAdmin(admin.ModelAdmin):
    model = OrderItemDownload
    list_display = ('id', 'profile', 'date', 'profile_ip')


class OrderItemIncomeInline(admin.TabularInline):
    model = OrderItemIncome
    extra = 1


class OrderItemAdmin(admin.ModelAdmin):
    inlines = [OrderItemIncomeInline]
    model = OrderItem
    list_display = ('id', 'order', 'beat', 'license')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderStripeInline(admin.StackedInline):
    model = OrderStripe


class OrderPaypalInline(admin.StackedInline):
    model = OrderPaypal


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderStripeInline, OrderPaypalInline, OrderItemInline]
    list_display = ('id', 'profile', 'date', 'status')


class BillingInfoAdmin(admin.ModelAdmin):
    list_display = ('profile',)


class AccountInvitationAdmin(admin.ModelAdmin):
    list_display = ('token', 'role', 'email_sent_to', 'name')


admin.site.register(Beat, BeatAdmin)
admin.site.register(LicenseOption, LicenseOptionAdmin)
admin.site.register(LicenseBought, LicenseBoughtAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Mood, MoodAdmin)
admin.site.register(TrendingBeat, TrendingBeatAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(FollowedProducer, FollowedProducerAdmin)
admin.site.register(FollowedPlaylist, FollowedPlaylistAdmin)
admin.site.register(LikedBeat, LikedBeatAdmin)
admin.site.register(Lyric, LyricAdmin)
admin.site.register(BeatKey, BeatKeyAdmin)
admin.site.register(ProducerPayout, ProducerPayoutAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemDownload, OrderItemDownloadAdmin)
admin.site.register(BillingInfo, BillingInfoAdmin)
admin.site.register(AccountInvitation, AccountInvitationAdmin)
