import requests
import stripe
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from sentry_sdk import capture_message
from stripe.api_resources.checkout import Session

from models.models import Order, OrderStripe
from payment_module.consts import STRIPE_SECRET_KEY
from settings.consts import APP_URL


def get_stripe():
    stripe.api_key = STRIPE_SECRET_KEY
    return stripe


def init_stripe_session(request: HttpRequest, order_id: int):
    # the order has to be pending
    pending_order: Order = get_object_or_404(Order, pk=order_id, status=Order.STATUS_PENDING,
                                             payment_platform=Order.PAYMENT_PLATFORM_CREDIT_CARD)
    
    try:
        stripe_customer = pending_order.profile.billinginfo.stripe_customer_id
        
        session: Session = get_stripe().checkout.Session.create(
            customer_email=pending_order.profile.billinginfo.email if stripe_customer is None else None,
            customer=stripe_customer,
            success_url=f'{APP_URL}/checkout/success/{pending_order.id}',
            cancel_url=f'{APP_URL}/checkout/cancel',
            payment_method_types=['card'],
            line_items=[
                {
                    'amount': int(item.license.price_discounted * 100),
                    'currency': 'usd',
                    'name': item.beat.name,
                    'description': item.license.name,
                    'images': [item.beat.image_url],
                    'quantity': 1,
                }
                for item in pending_order.items.all() if item.license.price_discounted > 0
            ],
            payment_intent_data={'metadata': {'order_id': int(pending_order.id)}}
        )
        
        OrderStripe.objects.create(order=pending_order, session_id=session.stripe_id)
        
        return JsonResponse(session)
    except stripe.error.InvalidRequestError as e:
        capture_message(f"Couldnt create Stripe session {e}", level="error")
        return HttpResponseBadRequest(f"Couldnt create Stripe session {e}")


def init_alipay_source(request: HttpRequest, order_id: int):
    pending_order: Order = get_object_or_404(Order, pk=order_id, status=Order.STATUS_PENDING,
                                             payment_platform=Order.PAYMENT_PLATFORM_ALIPAY)
    
    billing_info = pending_order.profile.billinginfo
    
    try:
        total_usd = pending_order.total
        conversion_rates: dict = requests.get(
            f'https://api.exchangeratesapi.io/latest?base=USD&symbols=CNY&access_key=be74184e1eccfafd2e8ef9993993b778').json()
        total_gbp = total_usd * conversion_rates['rates']['CNY']
        source = get_stripe().Source.create(
            type='alipay',
            currency='cny',
            amount=int(total_gbp * 100),
            owner={
                # 'address': billing_info.complete_address if billing_info.complete_address else None,
                'name': billing_info.full_name,
                'email': billing_info.email
            },
            redirect={'return_url': f'{APP_URL}/checkout/finish-alipay/{pending_order.id}'},
            metadata={'order_id': int(pending_order.id)}
        )
        
        OrderStripe.objects.create(order=pending_order, source_id=source.stripe_id)
        
        return JsonResponse(source)
    except stripe.error.InvalidRequestError as e:
        capture_message(f"Couldnt create Alipay source {e}", level="error")
        return HttpResponseBadRequest(f"Couldnt create Alipay source {e}")
