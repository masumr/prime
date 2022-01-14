import json

import paypalrestsdk
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sentry_sdk import capture_message

from email_module.views import send_emails_payment_successful
from models.models import Order
from payment_module.consts import STRIPE_WEBHOOK_SECRET, PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_ENVIROMENT
from payment_module.stripe_helper import get_stripe


@csrf_exempt
def webhook_stripe(request: HttpResponse):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    stripe = get_stripe()
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponseBadRequest('Invalid payload')
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest('Invalid signature')
    
    # Handle the checkout.session.completed event
    # if event['type'] == 'checkout.session.completed':
    #   session: stripe.api_resources.checkout.Session = event['data']['object']
    #   session_order_id = session['id']
    
    '''
    User accepted/completed the payment in Alipay's website, stripe sends this webhook
    which we use to create a charge and "bill" the user
    '''
    try:
        if event['type'] == 'source.chargeable':
            source = event['data']['object']
            stripe_source_id = source['id']
            
            stripe.Charge.create(
                amount=source['amount'],
                currency=source['currency'],
                source=stripe_source_id,
                metadata=source['metadata']
            )
        
        '''
        User either ends Alipay session, or there is an error in Alipay payment.
        '''
        # if event['type'] == 'source.canceled' or event['type'] == 'source.failed':
        
        # Handle the charge.succeeded
        if event['type'] == 'charge.succeeded':
            charge = event['data']['object']
            order_id = charge['metadata']['order_id']
            stripe_charge_id = charge['id']
            
            try:
                order: Order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return HttpResponseBadRequest(f'No order associated with that order_id: {order_id}')
            
            # save the changes and set the status to complete
            order.status = Order.STATUS_COMPLETE
            order.save()
            
            # save the changes and set the status to complete
            stripe_order = order.orderstripe
            # save here the charge id because metadata are lost on disputes
            stripe_order.charge_id = stripe_charge_id
            stripe_order.save()
            
            profile = order.profile
            profile.billinginfo.stripe_customer_id = charge['customer']
            
            # send email
            try:
                send_emails_payment_successful(user_email=profile.email, order=order)
            except Exception as e:
                capture_message(f'Error when sending mail {e}', level="error")
        
        # Handle the chargeback open
        if event['type'] == 'charge.dispute.created':
            order_charge_id = event['data']['object']['charge']
            
            try:
                order: Order = Order.objects.get(orderstripe__charge_id=order_charge_id)
            except Order.DoesNotExist:
                return HttpResponseBadRequest(f'No order associated with that order_charge_id: {order_charge_id}')
            
            # save the changes and set the status to reverse
            order.status = Order.STATUS_REVERSE
            order.save()
        
        # Handle the chargeback closed
        elif event['type'] == 'charge.dispute.closed':
            order_charge_id = event['data']['object']['charge']
            chargeback_status = event['data']['object']['chargeback_status']
            
            try:
                order: Order = Order.objects.get(orderstripe__charge_id=order_charge_id)
            except Order.DoesNotExist:
                return HttpResponseBadRequest(f'No order associated with that order_charge_id: {order_charge_id}')
            
            # save the changes and set the status to complete
            if chargeback_status in ['charge_refunded', 'lost']:
                order.status = Order.STATUS_REFUNDED
            elif chargeback_status in ['warning_closed', 'won']:
                order.status = Order.STATUS_COMPLETE
            
            order.save()
        
        return HttpResponse(status=200)
    except Exception as e:
        capture_message(e, level="error")
        return HttpResponseServerError(reason=e)


@csrf_exempt
def webhook_paypal(request: HttpResponse):
    payload = json.loads(request.body.decode('utf-8'))
    try:
        paypalrestsdk.configure({
            "mode": PAYPAL_ENVIROMENT,
            "client_id": PAYPAL_CLIENT_ID,
            "client_secret": PAYPAL_SECRET})
        
        # webhook_id = "BOH"
        # verify_response = WebhookEvent.verify(
        #     request.headers['Paypal-Transmission-Id'], request.headers['Paypal-Transmission-Time'], webhook_id, payload,
        #     request.headers['Paypal-Cert-Url'], request.headers['Paypal-Transmission-Sig'],
        #     request.headers['PayPal-Auth-Algo'])
        
        if payload['event_type'] in ['CUSTOMER.DISPUTE.CREATED', 'CUSTOMER.DISPUTE.UPDATED']:
            resource = payload['resource']
            # webhook_event = WebhookEvent(payload)
            # event_resource is wrapped the corresponding paypalrestsdk class
            # this is dynamically resolved by the sdk
            # event_resource = webhook_event.get_resource()
            
            seller_transaction_id = resource['disputed_transactions'][0]['seller_transaction_id']
            
            try:
                order: Order = Order.objects.get(orderpaypal__payment_capture_id=seller_transaction_id)
            except Order.DoesNotExist:
                return HttpResponseBadRequest(
                    f'No order associated with that seller_transaction_id: {seller_transaction_id}')
            
            # https://developer.paypal.com/docs/integration/direct/customer-disputes/webhooks/?mark=outcome#webhook-details
            if resource['status'] == 'OPEN':
                # save the changes and set the status to reverse
                order.status = Order.STATUS_REVERSE
                order.save()
                
            if resource['status'] == 'RESOLVED':
                dispute_outcome = resource['dispute_outcome']['outcome_code']
                
                if dispute_outcome in ['RESOLVED_SELLER_FAVOUR', 'CANCELED_BY_BUYER']:
                    order.status = Order.STATUS_COMPLETE
                    order.save()
                elif dispute_outcome in ['RESOLVED_BUYER_FAVOUR']:
                    order.status = Order.STATUS_REFUNDED
                    order.save()
        
        return JsonResponse({"boh": "bah"})
    except Exception as e:
        capture_message(e, level="error")
        return HttpResponseServerError(reason=e)
