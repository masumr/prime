import json
from datetime import datetime
from operator import itemgetter

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from analytics_module.consts import PERIOD_LAST_MONTH, PERIOD_LAST_SIX_MONTHS, PERIOD_ALL_TIME, ORDER_BY_PLAYS, \
    ORDER_BY_FOLLOWERS
from analytics_module.models import BeatPlay
from apis_admin.permissions.permissions import IsAdminOrIsProducer
from models.models import Playlist, FollowedPlaylist


@api_view(['POST'])
@login_required
@permission_classes((IsAdminOrIsProducer,))
def get_top_ten_playlists(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))
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

    if order_by == ORDER_BY_PLAYS:
        queryset_order_by = 'plays'
    elif order_by == ORDER_BY_FOLLOWERS:
        queryset_order_by = 'followers'
    else:
        return HttpResponseBadRequest('Filter unknown')
    xl = []
    for x in Playlist.objects.all():
        followed = FollowedPlaylist.objects.filter(playlist_id=x.id, date__gte=starting_date).count()
        plays = BeatPlay.objects.filter(beat__in=list(x.beats.all().values_list('id', flat=True)),
                                        date__gte=starting_date).count()
        data = {'id': x.id, "plays": plays, "followers": followed}
        xl.append(data)
    newlist = sorted(xl, key=itemgetter(queryset_order_by), reverse=True)
    return Response({'playlists': newlist[:10]})
