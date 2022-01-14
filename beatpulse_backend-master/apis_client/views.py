import json

from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle

from analytics_module.models import BeatPlay
from apis_client.serializer import CustomAppleSocialLoginSerializer
from models.models import Beat, Profile


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    client_class = AppleOAuth2Client
    callback_url = 'https://test-api.beatpulse.app/rest-auth/apple/'
    serializer_class = CustomAppleSocialLoginSerializer


@api_view(['POST'])
def get_beats_ids(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))
    filter_genres = data['filter_genres']
    filter_keys = data['filter_keys']
    filter_tempo = data['filter_tempo']

    queryset = Beat.objects.values('id').filter(is_published=True,
                                                bpm__gte=filter_tempo['min_bpm'],
                                                bpm__lte=filter_tempo['max_bpm'])
    if len(filter_genres) > 0:
        queryset = queryset.filter(genre__in=filter_genres)
    if len(filter_keys) > 0:
        queryset = queryset.filter(key__in=filter_keys)
    beats_ids = [beat['id'] for beat in queryset]
    return JsonResponse({'beats_ids': beats_ids})


@api_view(['POST'])
def set_email(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    password = data['password']
    profile: Profile = request.user

    if profile.is_social():
        return HttpResponseBadRequest("Social accounts can't change email")

    if not profile.check_password(password):
        return HttpResponseBadRequest('Invalid password')

    if profile.email == email:
        return HttpResponseBadRequest('the new mail is the same as the old one, nothing will be done')

    try:
        profile.add_email_address(request, email)
        return JsonResponse({"message": "ok"})
    except IntegrityError:
        return HttpResponseBadRequest('The email you entered is already registered, please try a different one.')


class TwicePerMinuteUserThrottle(UserRateThrottle):
    rate = '2/minute'


@api_view(['POST'])
@throttle_classes([TwicePerMinuteUserThrottle])
def api_increase_popularity_of_played_beat(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))
    beat: Beat = get_object_or_404(Beat, pk=data['beat_id'])
    BeatPlay.objects.create(beat=beat)
    return JsonResponse({"message": "ok"})
