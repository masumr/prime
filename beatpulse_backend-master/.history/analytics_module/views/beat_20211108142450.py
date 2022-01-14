from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Subquery, OuterRef
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from analytics_module.consts import PERIOD_LAST_MONTH, PERIOD_LAST_SIX_MONTHS, PERIOD_ALL_TIME, ORDER_BY_EARNINGS, \
    ORDER_BY_PLAYS, ORDER_BY_LIKES
from analytics_module.models import BeatPlay, BeatDemoDownload
from analytics_module.utils import SQCount
from analytics_module.views.generic import TotalView, DetailedView
from apis_admin.permissions.permissions import IsAdminOrIsProducer
from models.models import Order, OrderItem, Beat, Producer, LikedBeat


class TotalBeatView(TotalView):
    model = None

    def function_to_get_data(self, from_date, to_date):
        try:
            # if the request is made by the producer
            return self.model.objects.filter(date__gte=from_date,
                                             date__lte=to_date,
                                             beat__producers=self.request.user.producer).count()
        except Producer.DoesNotExist:
            # if it is made by the admin
            return self.model.objects.filter(date__gte=from_date, date__lte=to_date).count()


class DetailedBeatView(DetailedView):
    model = None

    def function_to_get_data_for_day(self, day):
        try:
            # if the request is made by the producer
            return self.model.objects.filter(date=day, beat__producers=self.request.user.producer).count()
        except Producer.DoesNotExist:
            # if it is made by the admin
            return self.model.objects.filter(date=day).count()

    def function_to_get_data_for_month(self, day):
        try:
            # if the request is made by the producer
            return self.model.objects.filter(date__lte=day,
                                             date__gt=day - relativedelta(months=1),
                                             beat__producers=self.request.user.producer).count()
        except Producer.DoesNotExist:
            # if it is made by the admin
            return self.model.objects.filter(date__lte=day,
                                             date__gt=day - relativedelta(months=1)).count()


class TotalBeatPlays(TotalBeatView):
    model = BeatPlay


class DetailedBeatPlays(DetailedBeatView):
    model = BeatPlay


class TotalBeatDemoDownloads(TotalBeatView):
    model = BeatDemoDownload


# class DetailedDemoDownloads(DetailedBeatView):
#     model = BeatDemoDownload


# class TotalBeatShares(TotalBeatView):
#     model = BeatShare
#
#
# class DetailedShares(DetailedBeatView):
#     model = BeatShare


# class TotalBeatLikes(TotalBeatView):
#     model = BeatLike
#
#
# class DetailedBeatLikes(DetailedBeatView):
#     model = BeatLike

class TotalBeatSold(TotalView):
    def function_to_get_data(self, from_date, to_date):
        try:
            # if the request is made by the producer
            return OrderItem.objects.filter(order__status=Order.STATUS_COMPLETE,
                                            order__date__date__gte=from_date,
                                            order__date__date__lte=to_date,
                                            beat__producers=self.request.user.producer).count()
        except Producer.DoesNotExist:
            # if it is made by the admin
            return OrderItem.objects.filter(order__status=Order.STATUS_COMPLETE,
                                            order__date__date__gte=from_date,
                                            order__date__date__lte=to_date).count()


@api_view(['POST'])
@login_required
@permission_classes((IsAdminOrIsProducer,))
def get_top_ten_beats(request: HttpRequest):
    data = request.data
    order_by = data['order_by']
    period = data['period']

    now = datetime.now().date()
    if period == PERIOD_LAST_MONTH:
        starting_date = datetime.now().date().replace(day=1)
    elif period == PERIOD_LAST_SIX_MONTHS:
        starting_date = now - relativedelta(months=6)
    elif period == PERIOD_ALL_TIME:
        starting_date = datetime(1970, 1, 1).date()
    else:
        return HttpResponseBadRequest('Period unknown')

    if order_by == ORDER_BY_EARNINGS:
        queryset_filters = {'earnings__isnull': False}
        queryset_order_by = '-earnings'
    elif order_by == ORDER_BY_PLAYS:
        queryset_filters = {'plays__isnull': False}
        queryset_order_by = '-plays'
    elif order_by == ORDER_BY_LIKES:
        queryset_filters = {'likes__isnull': False}
        queryset_order_by = '-likes'
    else:
        return HttpResponseBadRequest('Filter unknown')

    try:
        producer = request.user.producer
        queryset_filters['producers'] = producer
        annotate_earnings = Subquery(
            OrderItem.objects
                .filter(beat=OuterRef('pk'), producer_incomes__producer=producer)
                .exclude(order__date__date__lt=starting_date)
                .exclude(~Q(order__status=Order.STATUS_COMPLETE))
                .values('beat')
                .annotate(the_sum=Sum('producer_incomes__income'))
                .values('the_sum')[:1]
        )
        '''Sum('orderitem__producer_incomes__income',
                                filter=Q(orderitem__order__date__date__gte=starting_date,
                                         orderitem__producer_incomes__producer=producer))'''
    except Producer.DoesNotExist:
        annotate_earnings = Subquery(
            OrderItem.objects
                .filter(beat=OuterRef('pk'))
                .exclude(order__date__date__lt=starting_date)
                .exclude(~Q(order__status=Order.STATUS_COMPLETE))
                .values('beat')
                .annotate(the_sum=Sum('license__price_discounted'))
                .values('the_sum')[:1]
        )
        '''Sum('orderitem__license__price_discounted',
                                filter=Q(orderitem__order__date__date__gte=starting_date))'''
    plays = BeatPlay.objects.filter(beat_id=OuterRef('pk'), date__gte=starting_date)
    likes = LikedBeat.objects.filter(beat_id=OuterRef('pk'), date__gte=starting_date)

    queryset = Beat.objects.values('id') \
                   .annotate(plays=SQCount(plays),
                             likes=SQCount(likes),
                             earnings=annotate_earnings) \
                   .filter(**queryset_filters) \
                   .order_by(queryset_order_by)[:10]
    return Response({'beats': list(queryset)})
