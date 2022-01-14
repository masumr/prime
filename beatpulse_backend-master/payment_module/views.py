import json

from django.http import HttpRequest
from django.http import JsonResponse
from ipware import get_client_ip
from rest_framework.decorators import (api_view)

from models.models import LicenseOption, Beat, LicenseBought, Profile, Order, OrderItem, \
    OrderItemIncome
from payment_module.utils import create_cart


@api_view(['POST'])
def init_session(request: HttpRequest):
    profile: Profile = request.user
    data = json.loads(request.body.decode('utf-8'))
    
    # reset billing info full name if not present
    if not profile.billinginfo.full_name:
        profile.billinginfo.full_name = profile.first_name
        profile.billinginfo.save()
    
    # reset billing info email if not present
    if not profile.billinginfo.email:
        profile.billinginfo.email = profile.email
        profile.billinginfo.save()
    
    # billing info data
    profile_address = profile.billinginfo.complete_address
    # the cart with deals
    cart = create_cart(cart_items=profile.cartitem_set.all(), coupons=data['coupons'])
    # create a pending order
    client_ip, routable = get_client_ip(request)
    pending_order: Order = Order.objects.create(
        profile=profile,
        profile_ip=client_ip,
        profile_address=profile_address,
        profile_platform=data['profile_platform'],
        payment_platform=data['payment_platform'],
        profile_email=profile.billinginfo.email,
        total=cart.total
    )
    
    for item in cart.items:
        beat: Beat = Beat.objects.get(pk=item.beat_id)
        # the selected license
        selected_license: LicenseOption = LicenseOption.objects.get(pk=item.license_id)
        
        # the permanent saved license
        bought_license: LicenseBought = LicenseBought.objects.create(
            name=selected_license.name,
            price=selected_license.price,
            color_hex=selected_license.color_hex,
            is_featured=selected_license.is_featured,
            has_mp3=selected_license.has_mp3,
            has_wav=selected_license.has_wav,
            has_trackout=selected_license.has_trackout,
            description=selected_license.description,
            detailed_license_url=selected_license.detailed_license_url,
            contract_html=selected_license.contract_html,
            # real paid price
            price_discounted=item.license_discounted_price)
        
        order_item = OrderItem.objects.create(
            order=pending_order,
            beat=beat,
            license=bought_license
        )
        
        for beat_producer in beat.beatproducerrelation_set.all():
            # if a deal is buy 2 get 1 free
            # the producer of the free beat still should get 1/3
            # so we can't use the discounted price to the distribuied income
            
            percentage_of_total_without_discounts = item.license_price / cart.total_without_deals
            virtual_license_price = percentage_of_total_without_discounts * cart.total
            # producer_income = beat_producer.commission / 100.00 * item.license_discounted_price
            producer_income = beat_producer.commission / 100.00 * virtual_license_price
            
            OrderItemIncome.objects.create(
                order_item=order_item,
                producer=beat_producer.producer,
                income=producer_income,
            )
    
    return JsonResponse({"order_id": pending_order.id})
