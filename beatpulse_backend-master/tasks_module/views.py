from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Q
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest

from email_module.views import send_email_finish_checkout
from models.models import Profile, CartItem, TrendingBeat, Beat, Order
from payment_module.utils import create_cart


def update_trending_beats(request: HttpRequest):
    for period_value, period_description in TrendingBeat.PERIODS:
        
        # clear trending beats table
        query = TrendingBeat.objects.filter(period=period_value)
        old_trending_beats = list(query.values())
        query.delete()
        
        now = datetime.now().date()
        if period_value == TrendingBeat.PERIOD_TODAY:
            starting_date = now - timedelta(days=1)
        elif period_value == TrendingBeat.PERIOD_WEEK:
            starting_date = now - timedelta(days=7)
        elif period_value == TrendingBeat.PERIOD_MONTH:
            starting_date = now - relativedelta(months=1)
        elif period_value == TrendingBeat.PERIOD_YEAR:
            starting_date = now - relativedelta(years=1)
        elif period_value == TrendingBeat.PERIOD_ALL_TIME:
            starting_date = datetime(1970, 1, 1).date()
        else:
            return HttpResponseBadRequest('Period unknown for trending beats')
        
        beats = Beat.objects \
                    .annotate(popularity=Sum('beatpopularityincrease__increase_amount',
                                             filter=Q(beatpopularityincrease__date__gte=starting_date))) \
                    .filter(popularity__isnull=False, is_published=True) \
                    .order_by('-popularity')[:50]
        
        for index, beat in enumerate(beats):
            new_chart_position = index + 1
            trending_state = None
            # if the old trending list
            # find the beat in the old trending list
            first_beat_or_default = next((x for x in old_trending_beats if x['beat_id'] == beat.id), None)
            # if the beat is not present in the old trending list
            if first_beat_or_default is None:
                trending_state = TrendingBeat.STATE_NEW
            # if the new chart position is greater
            elif first_beat_or_default['index'] > new_chart_position:
                trending_state = TrendingBeat.STATE_UP
            # if the new chart position is the same
            elif first_beat_or_default['index'] == new_chart_position:
                trending_state = TrendingBeat.STATE_SAME
            # if hte new chart positon is smaller
            elif first_beat_or_default['index'] < new_chart_position:
                trending_state = TrendingBeat.STATE_DOWN
            # create a trending beat
            TrendingBeat.objects.create(beat=beat, period=period_value, state=trending_state,
                                        index=new_chart_position)
    return HttpResponse('Ok')


def check_for_abandoned_cart(request: HttpRequest):
    profiles = Profile.objects.all()
    the_good_day = datetime.now().date() - timedelta(days=2)
    for profile in profiles:
        cart_items = CartItem.objects.filter(profile=profile).order_by('-added_on_date')
        if cart_items.count() > 0 and cart_items[0].added_on_date == the_good_day:
            cart = create_cart(cart_items=cart_items, coupons=[])
            # send an email with the cart
            send_email_finish_checkout(user_email=profile.email, cart=cart)
    return HttpResponse('Ok')


def delete_old_pending_orders(request: HttpRequest):
    Order.objects.filter(status=Order.STATUS_PENDING, date__date__lt=datetime.today()).delete()
    return HttpResponse('Ok')

# def check_for_new_beats_from_following_producers(request: HttpRequest):
#     # get the artists that want to be notified
#     artists = UserArtist.objects.filter(email_subscription_active=True)
#     # for each artist
#     for artist in artists:
#         # producers that the user follows
#         producers_subscribed_to = FollowedProducer.objects \
#             .filter(artist=artist, should_receive_email=True) \
#             .values_list('producer_id', flat=True)
#         # new beats that were published recently
#         # and that the user want's to be notified about
#         new_beats = Beat.objects \
#             .filter(date_of_publishing=datetime.now().date() - timedelta(days=2),
#                     producer_id__in=producers_subscribed_to)
#         if new_beats.count() > 0:
#             # send the email
#             send_email_new_beats_from_followed_producers(user_email=artist.user.email, beats=new_beats)
