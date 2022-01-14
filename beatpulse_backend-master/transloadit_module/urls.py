from django.urls import path

from transloadit_module.views import encode_audio

urlpatterns = [
    path('encode_audio/', encode_audio),
]
