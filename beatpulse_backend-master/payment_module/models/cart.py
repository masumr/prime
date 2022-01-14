from typing import List

from payment_module.models.secure_cart_item import SecureCartItem


class Cart:
    def __init__(self, items: List[SecureCartItem]):
        self.items = items

    @property
    def total(self) -> float:
        """
        Calculates the total amount of the cart
        """

        def map_cart_item_to_price(cart_item: SecureCartItem):
            return cart_item.license_discounted_price

        return sum(map(map_cart_item_to_price, self.items))

    @property
    def total_without_deals(self) -> float:
        """
        Calculates the total amount of the cart without deals
        """
    
        def map_cart_item_to_price(cart_item: SecureCartItem):
            return cart_item.license_price
    
        return sum(map(map_cart_item_to_price, self.items))
