import json

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from sentry_sdk import capture_message
from transloadit import client

from amazons3_module.config_aws import AWS_UPLOAD_REGION, AWS_UPLOAD_ACCESS_KEY_ID, AWS_UPLOAD_SECRET_KEY, \
    AWS_BUCKET_PRIVATE
from apis_admin.permissions.permissions import CanUpload
from transloadit_module.config import TRANSLOADIT_KEY, TRANSLOADIT_SECRET


@api_view(['POST'])
@permission_classes((CanUpload,))
def encode_audio(request: HttpRequest):
    # the beat
    # beat: Beat = Beat.objects.get(pk=beat_id)
    body = json.loads(request.body.decode('utf-8'))
    original_file_path = body['filePath']
    should_convert_wav_to_mp3 = body['shouldConvertWavToMp3']
    should_convert_wav_to_ogg = False # should_convert_wav_to_mp3
    should_add_tag_file = body['shouldAddTagFile']
    
    tag_file_path: str = 'tags/Beatpulse_tags.mp3'
    
    # nothing to do here
    if should_add_tag_file is False and should_convert_wav_to_mp3 is False:
        return JsonResponse({'msg': 'Nothing to do here'})
    
    # export paths
    export_file_without_watermark_path = original_file_path.replace("wav", "mp3")
    export_file_ogg = original_file_path.replace("wav", "ogg")
    export_file_with_watermark_path = export_file_without_watermark_path.replace(".mp3", "-tagged.mp3")
    
    # https://transloadit.com/demos/file-importing/import-a-file-over-http/
    assembly = client.Transloadit(
        TRANSLOADIT_KEY, TRANSLOADIT_SECRET).new_assembly()
    
    # import the original track
    assembly.add_step(name='track_import', robot='/s3/import', options={
        'credentials': 'beatpulse_s3_robot_uploader',
        'path': original_file_path,
        'result': True
    })
    # if we should convert the wav to mp3
    if should_convert_wav_to_mp3:
        # convert to mp3
        assembly.add_step(name='mp3', robot='/audio/encode', options={
            'use': 'track_import',
            'result': True,
            'preset': 'mp3',
            'bitrate': 320000,
            'ffmpeg_stack': 'v3.3.3'
        })
    if should_convert_wav_to_ogg:
        # convert to ogg for streaming
        assembly.add_step(name='ogg_encoded', robot='/audio/encode', options={
            'use': 'track_import',
            "result": True,
            "ffmpeg_stack": "v3.3.3",
            # "ffmpeg": {
            #     "q:a": -1,
            #     "b:a": 62000,
            #     "ar": 22000
            # },
            "preset": "ogg",
            # 'bitrate': 320000,
        })
    # if we need to add the tag
    if should_add_tag_file:
        # import the watermark
        assembly.add_step(name='audio_import', robot='/s3/import', options={
            'credentials': 'beatpulse_s3_robot_uploader',
            'path': tag_file_path,
            'result': True
        })
        # merge the two files
        assembly.add_step(name='merge', robot='/audio/merge', options={
            'use': {
                'steps': [
                    {
                        # we use the converted wav if the producer uploaded a wav
                        # we use the uploaded mp3 if that is what the producer uploaded
                        'name': 'mp3' if should_convert_wav_to_mp3 else 'track_import',
                        'as': 'audio'
                    },
                    {
                        'name': 'audio_import',
                        'as': 'audio'
                    }
                ]
            },
            'duration': 'first',
            'result': True,
            'preset': 'mp3',
            'bitrate': 128000,
            'ffmpeg_stack': 'v3.3.3'
        })
        
        # export of the MP3 file with watermark
        assembly.add_step(name='export_private_tagged', robot='/s3/store', options={
            'use': ['merge'],
            'credentials': 'beatpulse_s3_robot_uploader',
            'path': export_file_with_watermark_path,
            'acl': 'private'
        })
    # if we converted an mp3
    if should_convert_wav_to_mp3:
        # export of the MP3 file without watermark
        assembly.add_step(name='export_private_mp3_untagged', robot='/s3/store', options={
            'use': ['mp3'],
            'credentials': 'beatpulse_s3_robot_uploader',
            'path': export_file_without_watermark_path,
            'acl': 'private'
        })
    if should_convert_wav_to_ogg:
        # export of the OGG for stream
        assembly.add_step(name='export_private_ogg', robot='/s3/store', options={
            'use': ['ogg_encoded'],
            'credentials': 'beatpulse_s3_robot_uploader',
            'path': export_file_ogg,
            'acl': 'private'
        })
    
    def _make_error(error):
        error_message = f'Error during transloading: {error}'
        capture_message(error_message, level="error")
        return JsonResponse({'msg': error_message}, status=400)
    
    # Start the Assembly
    try:
        assembly_response = assembly.create(retries=5, wait=True)
        if assembly_response.status_code == 200: #  and assembly_response.data['http_code'] == 200 removed in Transloadit API response
            return JsonResponse({
                'tagged_file_path': export_file_with_watermark_path,
                'mp3_file_path': export_file_without_watermark_path,
                'stream_file_path': None, # export_file_ogg,
                'msg': 'Converted files'
            })
        else:
            return _make_error(error=assembly_response.data)
    
    except Exception as e:
        return _make_error(error=e)
