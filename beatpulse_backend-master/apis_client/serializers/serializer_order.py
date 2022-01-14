from dynamic_rest.fields import SerializerMethodField, DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from apis_client.serializers.serializer_beat import BeatSerializer
from models.models import Order, OrderItem, LicenseBought, OrderStripe, OrderPaypal


class _OrderItemLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseBought
        fields = ('name', 'has_mp3', 'has_wav', 'has_trackout', 'price_discounted')


class _OrderItemSerializer(DynamicModelSerializer):
    beat = BeatSerializer(embed=True)
    license = _OrderItemLicenseSerializer()
    
    class Meta:
        model = OrderItem
        fields = OrderItem.public_fields


class OrderSerializer(DynamicModelSerializer):
    items = DynamicRelationField(_OrderItemSerializer, embed=True, many=True)
    # in the app, in the orders list we want to show images
    an_order_item_image = SerializerMethodField()
    total_discount = SerializerMethodField()
    payment_provider_charge_id = SerializerMethodField()
    
    @staticmethod
    def get_an_order_item_image(order: Order):
        return OrderItem.objects.filter(order=order).first().beat.image_thumbnail_url
    
    @staticmethod
    def get_total_discount(order: Order):
        return order.total_discount
    
    @staticmethod
    def get_payment_provider_charge_id(order: Order):
        try:
            charge_id = order.orderstripe.charge_id
        except OrderStripe.DoesNotExist:
            try:
                charge_id = order.orderpaypal.payment_capture_id
            except OrderPaypal.DoesNotExist:
                charge_id = None
        return charge_id
    
    class Meta:
        model = Order
        fields = Order.public_fields + ('items', 'an_order_item_image',)
        deferred_fields = (
            'items', 'an_order_item_image', 'profile_ip', 'profile_address', 'profile_email', 'total_discount',
            'payment_provider_charge_id')
