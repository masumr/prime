from django.db.models import Sum
from dynamic_rest.fields import DynamicRelationField, SerializerMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from apis_client.serializers.serializer_beat import BeatSerializer
from models.models import Order, OrderItem, OrderItemDownload, Profile, LicenseBought, OrderItemIncome, OrderStripe, \
    OrderPaypal


class _OrderItemLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseBought
        fields = ('name', 'has_mp3', 'has_wav', 'has_trackout', 'price_discounted')


class _OrderItemDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemDownload
        fields = OrderItemDownload.public_fields


class _OrderItemSerializer(DynamicModelSerializer):
    beat = BeatSerializer(embed=True)
    license = _OrderItemLicenseSerializer()
    downloads = _OrderItemDownloadSerializer(many=True)
    
    class Meta:
        model = OrderItem
        fields = OrderItem.public_fields


class _ProfileSerializer(DynamicModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name',)


class OrderSerializer(DynamicModelSerializer):
    profile = DynamicRelationField(_ProfileSerializer, embed=True)
    items = DynamicRelationField(_OrderItemSerializer, embed=True, many=True)
    quantity = SerializerMethodField()
    # total_gross = SerializerMethodField()
    producer_cut = SerializerMethodField()
    total_discount = SerializerMethodField()
    payment_provider_charge_id = SerializerMethodField()
    
    @staticmethod
    def get_quantity(order: Order):
        return order.items.count()
    
    # @staticmethod
    # def get_total_gross(order: Order):
    #    return OrderItem.objects.filter(order=order).aggregate(Sum('license__price_discounted'))[
    #        'license__price_discounted__sum']
    
    @staticmethod
    def get_producer_cut(order: Order):
        return OrderItemIncome.objects.filter(order_item__order=order).aggregate(Sum('income'))[
            'income__sum']
    
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
        fields = Order.public_fields_admin
        deferred_fields = ('items', 'payment_provider_charge_id')
