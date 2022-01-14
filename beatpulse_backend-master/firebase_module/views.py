import requests
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from analytics_module.models import BeatShare
from models.models import Beat, Producer, Playlist
from .consts import FIREBASE_API_URL


def _get_fireabase_post_data(ending_part_of_url: str):
    return {
        "dynamicLinkInfo": {
            "domainUriPrefix": "https://beatpulse.page.link",
            "link": f"https://beatpulse.app/{ending_part_of_url}",
            "androidInfo": {
                "androidPackageName": "app.beatpulseapp"
            },
            "iosInfo": {
                "iosBundleId": "app.beatpulse",
                "iosAppStoreId": "1439439035"
            },
            
            # https://firebase.google.com/docs/reference/dynamic-links/link-shortener
            # "analyticsInfo": {
            #     "googlePlayAnalytics": {
            #         "utmSource": string,
            #         "utmMedium": string,
            #         "utmCampaign": string,
            #         "utmTerm": string,
            #         "utmContent": string,
            #         "gclid": string
            #     },
            #     "itunesConnectAnalytics": {
            #         "at": string,
            #         "ct": string,
            #         "mt": string,
            #         "pt": string
            #     }
            # },
            # "socialMetaTagInfo": {
            # "socialTitle": string,
            # "socialDescription": string,
            # "socialImageLink": string
            # }
        },
        "suffix": {
            "option": "SHORT"
        }
    }


def _get_shareble_link(ending_part_of_url: str):
    json_response = requests.post(FIREBASE_API_URL, json=_get_fireabase_post_data(ending_part_of_url)).json()
    # error can be in the response
    return json_response['shortLink'] if 'shortLink' in json_response else None


def share_link(request: HttpRequest, model: str, pk: int):
    shareable_link = None
    if model == 'beat':
        beat: Beat = get_object_or_404(Beat, pk=pk)
        # for analytics
        BeatShare.objects.create(beat=beat)
        if beat.shareble_link:
            shareable_link = beat.shareble_link
        else:
            shareable_link = _get_shareble_link(f'beats/{pk}')
            beat.shareble_link = shareable_link
            beat.save()
    elif model == 'producer':
        producer: Producer = get_object_or_404(Producer, pk=pk)
        if producer.shareble_link:
            shareable_link = producer.shareble_link
        else:
            shareable_link = _get_shareble_link(f'producers/{pk}')
            producer.shareble_link = shareable_link
            producer.save()
    elif model == 'playlist':
        playlist: Playlist = get_object_or_404(Playlist, pk=pk)
        if playlist.shareble_link:
            shareable_link = playlist.shareble_link
        else:
            shareable_link = _get_shareble_link(f'playlists/{pk}')
            playlist.shareble_link = shareable_link
            playlist.save()
    return JsonResponse({'shareable_link': shareable_link})
