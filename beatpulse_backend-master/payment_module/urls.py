from django.urls import path

from payment_module.paypal_helper import init_paypal, paypal_capture_order
from payment_module.stripe_helper import (init_alipay_source,
                                          init_stripe_session)
from payment_module.views import init_session
from payment_module.webhooks import webhook_stripe, webhook_paypal

urlpatterns = [
    path('init_session/', init_session),
    path('init_stripe_session/<int:order_id>/', init_stripe_session),
    path('init_alipay_source/<int:order_id>/', init_alipay_source),
    path('webhook/stripe/', webhook_stripe),
    path('webhook/paypal/', webhook_paypal),
    path('init_paypal/<int:order_id>/', init_paypal),
    path('paypal_capture_order/<int:order_id>/<str:approved_order_id>/', paypal_capture_order),
]
