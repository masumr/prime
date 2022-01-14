import json

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt

from models.models import Producer, Profile, AccountInvitation, PLATFORM_WEB, GROUP_PRODUCER


def _pre_check_producer_existence(display_name: str, email: str):
    # check that there is not already a producer with that name or with that email
    if Producer.objects.filter(display_name__iexact=display_name).exists():
        raise Exception('display_name taken')
    elif Producer.objects.filter(profile__email=email).exists():
        raise Exception('email taken')

@csrf_exempt
def add_new_dashboard_user(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))
    invitation_token = data['invitation_token']
    invitation: AccountInvitation = get_object_or_404(AccountInvitation, token=invitation_token)
    full_name = invitation.name
    email = invitation.email_sent_to
    password = data['password']
    
    if invitation.role == GROUP_PRODUCER:
        try:
            _pre_check_producer_existence(display_name=data['display_name'], email=email)
        except Exception as e:
            return HttpResponseBadRequest(e)
    
    # let's find if another used has already signed up with that mail
    try:
        # if an artist with that mail already exists
        profile: Profile = Profile.objects.get(email=email)
    
    except Profile.DoesNotExist:
        # if not, we create an user with that credentials
        profile: Profile = Profile.objects.create_user(username=email,
                                                       email=email,
                                                       password=password,
                                                       first_name=full_name,
                                                       platform=PLATFORM_WEB)
        # attach the email address
        EmailAddress.objects.create(
            email=email,
            primary=True,
            user_id=profile.id
        )
        # send email confirmation
        send_email_confirmation(request=request, user=profile, signup=True)
    
    # set the group for permission
    new_group = get_object_or_404(Group, name=invitation.role)
    profile.groups.clear()
    profile.groups.add(new_group)
    
    if invitation.role == GROUP_PRODUCER:
        display_name = data['display_name']
        paypal_email = data['paypal_email']
        # create the producer account and attach it to the artist
        Producer.objects.create(
            profile=profile,
            display_name=display_name,
            slug=slugify(display_name),
            paypal_email=paypal_email
        )
    
    # in the end, delete the invitation
    invitation.delete()
    return HttpResponse('ok')
