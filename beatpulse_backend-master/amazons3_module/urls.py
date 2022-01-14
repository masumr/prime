from django.urls import path

from amazons3_module.views import sign_s3, api_beat_demo_download_link, beat_play, beat_download_link, sign_profile_avatar, \
    beat_offline_download_link

urlpatterns = [
    path('sign_s3/', sign_s3),
    path('sign_profile_avatar/', sign_profile_avatar),
    path('beat_demo_download_link/<int:beat_id>/', api_beat_demo_download_link),
    path('beat_offline_download_link/<int:beat_id>/', beat_offline_download_link),
    path('beat_play/<int:beat_id>/', beat_play),
    # path('beat_play_link/<int:beat_id>/', beat_play_link),
    path(
        'beat_download_link/<int:beat_id>/<str:file_type>/', beat_download_link),
]
