import sys

from django.http import (HttpRequest, HttpResponseBadRequest,
                         JsonResponse)
from django.shortcuts import get_object_or_404
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest, OrdersCreateRequest
from sentry_sdk import capture_message

from email_module.views import send_emails_payment_successful
from models.models import Order, OrderPaypal, Profile
from payment_module.consts import PAYPAL_CLIENT_ID, PAYPAL_SECRET
from settings.consts import APP_URL
from settings.settings_base import STAGING

"""
DOCS
https://github.com/paypal/Checkout-Python-SDK#capturing-an-order
https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/
https://developer.paypal.com/docs/api/orders/v2/
"""


class PayPalClient:
    def __init__(self):
        self.client_id = PAYPAL_CLIENT_ID
        self.client_secret = PAYPAL_SECRET
        
        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use ProductionEnvironment."""
        if STAGING:
            self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        else:
            self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)


# Construct a request object and set desired parameters
# Here, OrdersCreateRequest() creates a POST request to /v2/checkout/orders
def init_paypal(_: HttpRequest, order_id: int):
    paypal_client_instance = PayPalClient()
    
    # the order has to be pending
    pending_order: Order = get_object_or_404(Order, pk=order_id, status=Order.STATUS_PENDING,
                                             payment_platform=Order.PAYMENT_PLATFORM_PAYPAL)
    
    request = OrdersCreateRequest()
    request.prefer('return=representation')
    
    request.request_body(
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "custom_id": str(pending_order.id),
                    "amount": {
                        "currency_code": "USD",
                        "value": f'{pending_order.total:.2f}',
                        "breakdown": {
                            "item_total": {
                                "currency_code": "USD",
                                "value": f'{pending_order.total:.2f}'
                            },
                        },
                    },
                    "items": [
                        {
                            "unit_amount": {
                                "currency_code": "USD",
                                "value": f'{item.license.price_discounted:.2f}'
                            },
                            "name": item.beat.name[:126],
                            "description": item.license.name,
                            "sku": str(item.beat.id),
                            "quantity": "1",
                            "category": "DIGITAL_GOODS"
                        }
                        for item in pending_order.items.all() if item.license.price_discounted > 0
                    ],
                }
            ],
            "application_context": {
                "landing_page": "BILLING",
                "user_action": 'PAY_NOW',
                "return_url": f'{APP_URL}/checkout/finish-paypal/{order_id}',
                "cancel_url": f'{APP_URL}/checkout/cancel/',
            }
        }
    )
    
    try:
        # Call API with your client and get a response for your call
        response = paypal_client_instance.client.execute(request)
        return JsonResponse({'link': response.result.links[1].href})
    
    except IOError as ioe:
        # return HttpResponseBadRequest('Error during payment creation')
        return JsonResponse({'message': ioe.message}, status=ioe.status_code)


def paypal_capture_order(_, order_id: int, approved_order_id: str):
    paypal_client_instance = PayPalClient()
    
    try:
        order: Order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest(f'No order associated with that order_id: {order_id}')
    
    try:
        request = OrdersCaptureRequest(approved_order_id)
        # Call API with your client and get a response for your call
        response = paypal_client_instance.client.execute(request)
        # save the changes and set the status to complete
        order.status = Order.STATUS_COMPLETE
        order.save()
        
        # OrderPaypal.objects.create(order=order, charge_id=approved_order_id)
        OrderPaypal.objects.create(order=order,
                                   paypal_order_id=response.result.id,
                                   payment_capture_id=response.result.purchase_units[0].payments.captures[0].id,
                                   json_result={"approved_order_id": approved_order_id})
        
        # send email
        try:
            profile: Profile = order.profile
            
            send_emails_payment_successful(user_email=profile.email, order=order)
        except Exception as e:
            capture_message(f'Error when sending mail {e}', level="error")
        
        return JsonResponse({'message': 'ok'})
    
    except IOError as ioe:
        # return HttpResponseBadRequest(f'Error during payment capture')
        return JsonResponse({'message': ioe.message}, status=ioe.status_code)
