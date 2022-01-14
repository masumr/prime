import datetime
import json
import os
import uuid
from os.path import basename

from botocore.signers import CloudFrontSigner
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from ipware import get_client_ip
from rest_framework.decorators import api_view, permission_classes

from amazons3_module.cloudfront import CLOUDFRONT_PRIVATE_URL
from amazons3_module.utils import get_s3, fix_amazon_url, rsa_signer
from analytics_module.models import BeatDemoDownload
from apis_admin.permissions.permissions import CanUpload
from models.models import Beat, OrderItem, OrderItemDownload, Order
from settings.consts import MP3_FILE_TYPE, WAV_FILE_TYPE, TRACKOUT_FILE_TYPE, TAGGED_FILE_TYPE
from .config_aws import (AWS_BUCKET, AWS_BUCKET_PRIVATE)


@api_view(['POST'])
@permission_classes((CanUpload,))
def sign_s3(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))
    file_name: str = data['file_name']
    # application/pdf for pdf
    file_type: str = data['file_type']
    upload_type: str = data['upload_type']
    # define folder structure
    is_a_beat = upload_type in [TAGGED_FILE_TYPE, MP3_FILE_TYPE, WAV_FILE_TYPE, TRACKOUT_FILE_TYPE]
    is_an_image = upload_type == 'image'
    if is_a_beat:
        dir_name = 'beats'
    else:
        dir_name = 'assets'
    file_path = f'{dir_name}/{uuid.uuid4()}/{file_name}'
    fields = {'Content-Type': file_type}
    conditions = [{'Content-Type': file_type}]  # , {'x-amz-storage-class': 'INTELLIGENT_TIERING'}
    # if it is an image or a pdf
    if file_type in ['application/pdf'] or is_an_image:
        bucket = AWS_BUCKET
    else:
        bucket = AWS_BUCKET_PRIVATE
    # generate_presigned_post
    presigned_post = get_s3().generate_presigned_post(
        Bucket=bucket,
        Key=file_path,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=36000
    )
    # fix amazon url
    presigned_post['url'] = fix_amazon_url(presigned_post['url'])
    return JsonResponse(presigned_post)


@api_view(['POST'])
def sign_profile_avatar(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))
    file_name = os.path.basename(data['file_name'])
    profile_id = request.user.id
    presigned_post = get_s3().generate_presigned_post(
        Bucket=AWS_BUCKET,
        Key=f'profiles-assets/{profile_id}/{uuid.uuid4()}-{file_name}',
        Fields={'Content-Type': 'image/*'},
        Conditions=[{'Content-Type': 'image/*'}]
    )
    # fix amazon url
    presigned_post['url'] = fix_amazon_url(presigned_post['url'])
    return JsonResponse(presigned_post)


def beat_play(request: HttpRequest, beat_id: int):
    # the beat to listen to
    beat: Beat = get_object_or_404(Beat, pk=beat_id)
    # the path in amazon s3
    # if the beat has not tagged file, we send the mp3 file
    # file_path = f'{beat.tagged_file_path if beat.tagged_file_path else beat.mp3_file_path}'
    file_path = beat.stream_file_path if beat.stream_file_path else beat.mp3_file_path
    if not file_path:
        return HttpResponseBadRequest('the beat has no ogg or mp3 file uploaded')
    
    key_id = 'APKAIPYEW3XOZLF654EA'
    url = f'{CLOUDFRONT_PRIVATE_URL}/{file_path}'
    current_time = datetime.datetime.utcnow()
    expire_date = current_time + datetime.timedelta(minutes=60)
    cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)
    # Create a signed url that will be valid until the specfic expiry date
    # provided using a canned policy.
    signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
    return HttpResponseRedirect(fix_amazon_url(signed_url))


# def beat_play_link(request: HttpRequest, beat_id: int):
#     # the beat to listen to
#     beat: Beat = get_object_or_404(Beat, pk=beat_id)
#     # the path in amazon s3
#     # if the beat has not tagged file, we send the mp3 file
#     # file_path = f'{beat.tagged_file_path if beat.tagged_file_path else beat.mp3_file_path}'
#     file_path = beat.mp3_file_path
#     if not file_path:
#         return HttpResponseBadRequest('the beat has no mp3 file uploaded')
#
#     key_id = 'APKAIPYEW3XOZLF654EA'
#     url = f'{CLOUDFRONT_PRIVATE_URL}/{file_path}'
#     current_time = datetime.datetime.utcnow()
#     expire_date = current_time + datetime.timedelta(minutes=60)
#     cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)
#     # Create a signed url that will be valid until the specfic expiry date
#     # provided using a canned policy.
#     signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
#     return JsonResponse({'url': fix_amazon_url(signed_url)})


def _abstract_beat_download_without_license_link(file_path: str):
    return get_s3().generate_presigned_url(
        'get_object', Params={'Bucket': AWS_BUCKET_PRIVATE, 'Key': file_path,
                              'ResponseContentDisposition': f'attachment;filename="{basename(file_path)}"',
                              'ResponseContentType': 'application/octet-stream'
                              })


def get_beat_demo_download_link(beat_id: int):
    beat: Beat = get_object_or_404(Beat, pk=beat_id)
    # for analytics
    BeatDemoDownload.objects.create(beat=beat)
    return _abstract_beat_download_without_license_link(beat.tagged_file_path)


def api_beat_demo_download_link(request: HttpRequest, beat_id: int):
    return JsonResponse({'url': get_beat_demo_download_link(beat_id=beat_id)})


def beat_offline_download_link(request: HttpRequest, beat_id: int):
    beat: Beat = get_object_or_404(Beat, pk=beat_id)
    return JsonResponse({'url': _abstract_beat_download_without_license_link(beat.mp3_file_path)})


@api_view(['GET'])
def beat_download_link(request: HttpRequest, beat_id: int, file_type: str):
    beat: Beat = get_object_or_404(Beat, pk=beat_id)
    is_external_to_amazon = False
    
    # check if the license covers the requested file type
    if file_type == TAGGED_FILE_TYPE:
        file_path = beat.tagged_file_path
    elif file_type == MP3_FILE_TYPE:
        file_path = beat.mp3_file_path
    elif file_type == WAV_FILE_TYPE:
        file_path = beat.wav_file_path
    elif file_type == TRACKOUT_FILE_TYPE:
        if beat.trackout_file_path:
            file_path = beat.trackout_file_path
        else:
            file_path = beat.trackout_external_url
            is_external_to_amazon = True
    else:
        return HttpResponseBadRequest('unknown file type')
    
    if not file_path:
        return HttpResponseBadRequest('the beat does not have that file type')
    
    if not request.user.is_admin():
        filters = {
            'beat': beat,
            'order__profile': request.user,
            'order__status': Order.STATUS_COMPLETE
        }
        if file_type == MP3_FILE_TYPE:
            filters['license__has_mp3'] = True
        elif file_type == WAV_FILE_TYPE:
            filters['license__has_wav'] = True
        elif file_type == TRACKOUT_FILE_TYPE:
            filters['license__has_trackout'] = True
        
        try:
            # track downloads, but not for the links generated after order completed
            order_item: OrderItem = OrderItem.objects.filter(**filters).first()
            client_ip, routable = get_client_ip(request)
            OrderItemDownload.objects.create(order_item=order_item, profile=request.user, profile_ip=client_ip)
        except OrderItem.DoesNotExist:
            return HttpResponseBadRequest('no license found that covers the download of that type of beat')
    
    if is_external_to_amazon:
        return JsonResponse({'url': file_path})
    else:
        if file_type in [MP3_FILE_TYPE, WAV_FILE_TYPE]:
            if file_type == MP3_FILE_TYPE:
                beat_extension = 'mp3'
            else:
                beat_extension = 'wav'
            filename = f'beatpulse_{beat.name}_{beat.bpm}bpm_{beat.key.name}.{beat_extension}'
        else:
            filename = basename(file_path)
        
        # generate a url that expires
        presigned_url = get_s3().generate_presigned_url(
            'get_object', Params={'Bucket': AWS_BUCKET_PRIVATE, 'Key': file_path,
                                  'ResponseContentDisposition': f'attachment;filename="{filename}"',
                                  'ResponseContentType': 'application/octet-stream'
                                  })
        
        return JsonResponse({'url': fix_amazon_url(presigned_url)})

# def show_license_pdf(request: HttpRequest, order_item_id: int):
# producer = UserProducer.objects.get(slug=producer_slug)
# # if the producer uploaded the summary pdf we show that
# if producer.license_summary_pdf:
#     file_path = producer.license_summary_pdf
#     return HttpResponseRedirect(file_path)
# # otherwise we generate one by merging his contracts in 1 file
# else:
#     license_options = LicenseOption.objects.filter(userproducer=producer.id).order_by('value')
#     return generate_license_summary_pdf(license_options=license_options)
