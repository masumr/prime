from django.urls import path

from pdf_module.views import generate_contract_pdf, generate_producer_payout_pdf

urlpatterns = [
    path(
        'generate_contract_pdf/<int:order_item_id>/<str:filename>', generate_contract_pdf),
    path('generate_producer_payout_pdf/<int:producer_payout_id>/', generate_producer_payout_pdf),
]
