import json

import requests
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from ipware import get_client_ip

from settings.consts import IP_INFO_TOKEN


def _set_custom_data_for_user(request, user, data):
    country = ''
    client_ip, routable = get_client_ip(request)
    if client_ip is not None:
        # we have a real, public ip address for user
        ip_data: dict = requests.get(
            f'https://ipinfo.io/{client_ip}/json?token={IP_INFO_TOKEN}').json()
        if 'country' in ip_data:
            country = ip_data['country']
    user_field(user, 'country', country)
    user_field(user, 'platform', data.get('platform', ''))
    user_field(user, 'image_avatar_file_path', data.get('image_avatar_file_path', None))


class CustomUserAccountAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        user = super().save_user(request, user, form, False)
        user_field(user, 'first_name', request.data.get('first_name', ''))
        _set_custom_data_for_user(request, user, request.data)
        user.save()
        return user


class CustomSocialAdapter(DefaultSocialAccountAdapter):
    
    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.
    
        For convenience, we populate several common fields.
    
        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.
    
        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        # fix because sometimes usernames are empty
        data['username'] = data['email']
        user = super().populate_user(request, sociallogin, data)
        _set_custom_data_for_user(request, user, data)
        return user
