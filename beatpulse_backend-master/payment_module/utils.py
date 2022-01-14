from datetime import datetime
from typing import List

from django.db.models import Q, QuerySet

from models.models import Coupon, Deal
from payment_module.models.cart import Cart
from payment_module.models.secure_cart_item import SecureCartItem


def _cart_items_for_deal(cart_items: List[SecureCartItem], deal: Deal) -> List[SecureCartItem]:
    deal_excluded_licenses = [x.id for x in deal.excluded_licenses.all()]
    return [x for x in cart_items if x.license_id not in deal_excluded_licenses]


def create_cart(cart_items: QuerySet, coupons: List[dict]) -> Cart:
    secure_cart_items: List[SecureCartItem] = []
    # for each cart item
    for cart_item in cart_items:
        # create an object representing the cart item
        secure_cart_item = SecureCartItem(beat_id=cart_item.beat.id,
                                          license_id=cart_item.license_option.id,
                                          license_price=cart_item.license_option.price,
                                          license_discounted_price=cart_item.license_option.price,
                                          db_id=cart_item.id)

        secure_cart_items.append(secure_cart_item)
    # sort by license value, then by price
    secure_cart_items = sorted(secure_cart_items, key=lambda x: -x.license_discounted_price)

    # get the best deal that is possible to activate
    deals = Deal.objects.all()
    sorted(deals, key=lambda deal: deal.needed_beats())
    good_deals = [deal for deal in deals if deal.needed_beats() <= len(_cart_items_for_deal(secure_cart_items, deal))]
    active_deal = good_deals[0] if len(good_deals) > 0 else None

    if active_deal is not None:
        cart_items_for_deal = _cart_items_for_deal(secure_cart_items, active_deal)
        n_of_cart_items_for_deal = len(cart_items_for_deal)
        needed_beats_for_bundle = active_deal.needed_beats()
        beats_not_in_bundle = n_of_cart_items_for_deal % needed_beats_for_bundle
        n_of_bundles = (n_of_cart_items_for_deal - beats_not_in_bundle) // needed_beats_for_bundle
        beats_to_pay = beats_not_in_bundle + n_of_bundles * active_deal.buy
        for index, cart_item in enumerate(cart_items_for_deal):
            if index >= beats_to_pay:
                cart_item.license_discounted_price = 0
    elif coupons:
        try:
            coupon: Coupon = Coupon.objects.filter(Q(token__in=[x['token'] for x in coupons]),
                                                   Q(expiration_date__gt=datetime.now()) | Q(
                                                       expiration_date=None)).first()
            # for each cart item
            for cart_item in secure_cart_items:
                # if a discount contains the license of the beat
                coupon_licenses_ids = map(lambda x: x.id, coupon.licenses.all())
                if cart_item.license_id in coupon_licenses_ids:
                    # from the price substract the discount
                    cart_item.license_discounted_price -= (
                        cart_item.license_discounted_price / 100 * coupon.discount_percentage)
        except Coupon.DoesNotExist:
            # the coupon doesnt exist, strange..
            pass
    return Cart(items=secure_cart_items)
