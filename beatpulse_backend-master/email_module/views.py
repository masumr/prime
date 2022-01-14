from datetime import datetime
from typing import List

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Email

from amazons3_module.views import get_beat_demo_download_link
from email_module.consts import SENDGRID_API_KEY
from models.models import Order, OrderItem, Beat, LicenseOption, ProducerPayout
from models.models import Producer
# from models.models import Producer, Beat, CoProducerOfBeat, UserArtist
# from django_models.secure_cart_item import SecureCartItem
from payment_module.models.cart import Cart
from settings.consts import APP_URL, APP_API_URL
from settings.settings_base import STAGING, PRODUCTION


def send_email_finish_checkout(user_email: str, cart: Cart):
    # who to send the mail
    to = 'developer@beatpulse.app' if STAGING else user_email
    # the subject
    subject = 'You left something behind'
    # the template name
    template_name = 'customer-abandoned-cart.html'
    # we have to convert the cart for the html of the mail
    cart_items = []
    for item in cart.items:
        cart_items.append({
            'beat': Beat.objects.get(pk=item.beat_id),
            'license_option': LicenseOption.objects.get(pk=item.license_id),
            'license_discounted_price': item.license_discounted_price
        })
    # the data to render the template
    template_data = {'cart_items': cart_items}
    # send the mail to the artist
    send_email(to=to, subject=subject, template_name=template_name,
               template_data=template_data)


def send_emails_payment_successful(user_email: str, order: Order):
    # send the mail to the artist and the producers
    send_email_customer_order_link(user_email=user_email, order_id=order.id)
    send_email_producers_order(order=order)


@api_view(['GET'])
def api_send_email_customer_order_link(request: HttpRequest, order_id: int):
    order: Order = get_object_or_404(Order, pk=order_id)
    send_email_customer_order_link(user_email=order.profile_email, order_id=order_id)
    return JsonResponse({'message': 'Ok'})


def send_email_customer_order_link(user_email: str, order_id: int):
    # who to send the mail
    to = 'developer@beatpulse.app' if STAGING else user_email
    # the subject
    subject = 'Order Review - Successful purchase'
    # the template name
    template_name = 'customer-order-link.html'
    # the data to render the template
    template_data = {
        'order_id': order_id,
        'order_id_with_leading_zeros': str(order_id).zfill(4),
        'url': f'{APP_URL}/order/{order_id}/'
    }
    # send the mail to the artist
    send_email(to=to, subject=subject, template_name=template_name, template_data=template_data,
               send_also_to_beatpulse=PRODUCTION)


def send_email_producers_order(order: Order):
    producers: List[Producer] = Producer.objects.filter(beat__orderitem__order=order).distinct()
    order_id_with_leading_zeros = str(order.id).zfill(4)
    now = datetime.now().strftime("%B %d, %Y")
    # for each producer
    for producer in producers:
        # producer order passed to html
        total_revenue = 0
        producer_order = {'id_with_leading_zeros': order_id_with_leading_zeros, 'date': now, 'total_revenue': 0,
                          'items': []}
        # get the cart items of the producer
        order_items: List[OrderItem] = order.items.filter(producer_incomes__producer=producer)
        for item in order_items:
            revenue = item.producer_incomes.get(producer=producer).income
            # for each item
            producer_order['items'].append({
                'beat_image_url': item.beat.image_thumbnail_url,
                'beat_name': item.beat.name,
                'license_name': item.license.name,
                'license_price': f"{item.license.price:.2f}"
            })
            total_revenue += revenue
            # calculate producer commission
        producer_order['total_revenue'] = f"{total_revenue:.2f}"
        # send a mail
        # who to send the mail
        to = 'developer@beatpulse.app' if STAGING else producer.contact_email
        # the subject
        subject = f"Beatpulse - Order: #{order_id_with_leading_zeros}"
        # the template name
        template_name = 'producer-order-notification.html'
        # the data to render the template
        template_data = {'order': producer_order}
        # send the mail to the artist
        send_email(to=to, subject=subject, template_name=template_name, template_data=template_data,
                   send_also_to_beatpulse=PRODUCTION)


def send_email_producer_invite(email_sent_to: str, role: str, token):
    # who to send the mail
    to = email_sent_to
    # the subject
    subject = 'You have been invited to join Beatpulse'
    # the template name
    template_name = 'producer-registration-link.html'
    # the data to render the template
    template_data = {'role': role, 'token': token}
    # send the mail
    return send_email(to=to, subject=subject, template_name=template_name, template_data=template_data)


@api_view(['GET'])
def api_send_email_payout_invoice_to_producer(request: HttpRequest, producer_payout_id: int):
    producer_payout: ProducerPayout = get_object_or_404(ProducerPayout, pk=producer_payout_id)
    # who to send the mail
    to = 'developer@beatpulse.app' if STAGING else producer_payout.producer.profile.email
    # the subject
    subject = 'Download Payout Invoice'
    # the template name
    template_name = 'producer-payout-invoice.html'
    # the data to render the template
    template_data = {
        'payout': producer_payout,
        'payout_url': f'{APP_API_URL}/pdf/generate_producer_payout_pdf/{producer_payout_id}/'
    }
    # send the mail to the artist
    send_email(to=to, subject=subject, template_name=template_name, template_data=template_data)
    return JsonResponse({'message': 'Ok'})


@api_view(['GET'])
def api_send_demo_download_link(request: HttpRequest, beat_id: int):
    beat: Beat = get_object_or_404(Beat, pk=beat_id)
    # who to send the mail
    to = request.user.email
    # the subject
    subject = f'Demo Download of "{beat.name}"'
    # the template name
    template_name = 'demo-download-link.html'
    # the data to render the template
    template_data = {
        'beat_name': beat.name,
        'download_url': get_beat_demo_download_link(beat_id=beat_id)
    }
    # send the mail to the artist
    send_email(to=to, subject=subject, template_name=template_name, template_data=template_data)
    return JsonResponse({'message': 'Ok'})


@api_view(['GET'])
def api_test(request: HttpRequest):
    # who to send the mail
    to = 'globlagency@gmail.com'
    # the subject
    subject = 'TEST'
    # the template name
    template_name = 'producer-payout-invoice.html'
    # the data to render the template
    template_data = {
    }
    # send the mail to the artist
    send_email(to=to, subject=subject, template_name=template_name, template_data=template_data,
               send_also_to_beatpulse=True)
    return JsonResponse({'message': 'Ok'})


def send_email(to: str, subject: str, template_name: str, template_data: dict, from_email: str = None,
               send_also_to_beatpulse=False):
    """
    method to send an email
    :param to: who to send the mail to
    :param subject: the subject
    :param template_name: the template name
    :param template_data: the data to render the template
    :param from_email: who sent the mail
    :return: an @HttpResponse with the body of the result from SendGrid
    """
    # api key
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    # from
    _from_email = Email(
        email=from_email if from_email else 'no-reply@beatpulse.co', name='Beatpulse')
    # to
    _to_email = to
    # render the html to replace the dynamic data
    rendered = render_to_string(f'sendgrid/{template_name}', template_data)
    # content type
    _content = Content('text/html', rendered)
    # email object
    _mail = Mail(from_email=_from_email, subject=subject, to_emails=_to_email, html_content=_content)
    if send_also_to_beatpulse:
        _mail.add_bcc('info@beatpulse.co')
    # response from send grid
    response = sg.send(_mail)
    # return
    return HttpResponse(response.body)
