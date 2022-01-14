from django.urls import path

from apis_client.views import get_beats_ids, set_email, api_increase_popularity_of_played_beat

urlpatterns = [
    path('get_beats_ids/', get_beats_ids),
    path('set_profile_email/', set_email),
    path('api_increase_popularity_of_played_beat/', api_increase_popularity_of_played_beat),
]
