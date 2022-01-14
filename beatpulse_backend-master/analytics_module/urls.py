from django.urls import path

from analytics_module.views.beat import TotalBeatPlays, DetailedBeatPlays, TotalBeatDemoDownloads, TotalBeatSold, \
    get_top_ten_beats
from analytics_module.views.producer_own_followers import TotalProducerOwnFollowers, DetailedProducerOwnFollowers
from analytics_module.views.playlist import get_top_ten_playlists
from analytics_module.views.sales import DetailedSales, TotalSales, TotalNetSales, TotalProducerPayouts
from analytics_module.views.signups import TotalSignups, DetailedSignups

urlpatterns = [
    # beat
    path('total_beat_plays/', TotalBeatPlays.as_view()),
    path('detailed_beat_plays/', DetailedBeatPlays.as_view()),
    path('total_beat_demo_downloads/', TotalBeatDemoDownloads.as_view()),
    path('total_beat_sold/', TotalBeatSold.as_view()),
    path('top_ten_beats/', get_top_ten_beats),
    # playlists
    path('top_ten_playlists/', get_top_ten_playlists),
    # sales
    path('total_sales/', TotalSales.as_view()),
    path('detailed_sales/', DetailedSales.as_view()),
    path('total_net_sales/', TotalNetSales.as_view()),
    path('total_producer_payouts/', TotalProducerPayouts.as_view()),
    # signups
    path('total_signups/', TotalSignups.as_view()),
    path('detailed_signups/', DetailedSignups.as_view()),
    # own producer followers
    path('total_producer_own_followers/', TotalProducerOwnFollowers.as_view()),
    path('detailed_producer_own_followers/', DetailedProducerOwnFollowers.as_view()),
]
