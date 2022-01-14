from django.urls import path

from email_module.views import api_send_email_customer_order_link, api_send_email_payout_invoice_to_producer, api_test, \
    api_send_demo_download_link

urlpatterns = [
    path('api_send_email_customer_order_link/<int:order_id>/', api_send_email_customer_order_link),
    path('api_send_email_payout_invoice_to_producer/<int:producer_payout_id>/',
         api_send_email_payout_invoice_to_producer),
    path('api_send_demo_download_link/<int:beat_id>/', api_send_demo_download_link),
    path('api_test/', api_test),
]
