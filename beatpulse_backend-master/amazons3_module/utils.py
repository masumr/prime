import os

import boto3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from settings.settings_base import BASE_DIR
from .config_aws import (AWS_UPLOAD_ACCESS_KEY_ID,
                         AWS_UPLOAD_REGION, AWS_UPLOAD_SECRET_KEY)


def get_s3():
    return boto3.client('s3',
                        aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_UPLOAD_SECRET_KEY,
                        region_name=AWS_UPLOAD_REGION)


def fix_amazon_url(url):
    """
    This motherfuckers can't return urls
    :param url: the incorrect url
    :return: the correct url
    """
    if url.endswith('/'):
        url = url[:-1]
    url = url \
        .replace("#", "%23")
    return url


def is_image(key: str):
    return key.endswith(('jpeg', 'jpg', 'png'))


def generate_beat_folder_name(producer_id: int, file_name: str = 'unknown name', beat_name: str = '') -> str:
    # if we have a beat name
    if beat_name:
        return f'producers/{producer_id}/beats/{beat_name}' \
            .replace('w/', 'w')
    # if we have a file name
    else:
        for char in ['(', ')', '[', ']', '\'', '"']:
            file_name = file_name.replace(char, '')
        file_name = os.path.splitext(file_name)[0] \
            .replace(" ", "-") \
            .replace("%20", "-") \
            .replace('%27', '') \
            .replace("'", '') \
            .replace("--", "-").lower()
        return f'producers/{producer_id}/beats/{file_name}'


def rsa_signer(message):
    with open(os.path.join(BASE_DIR, 'amazons3_module/pk-APKAIPYEW3XOZLF654EA.pem'), 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
