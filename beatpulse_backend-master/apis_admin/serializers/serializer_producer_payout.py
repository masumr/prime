from typing import List

from django.utils import timezone
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from models.models import ProducerPayoutDescriptionField, ProducerPayout, OrderItem, Order


class _ProducerPayoutDescriptionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerPayoutDescriptionField
        fields = ('description', 'amount')


class ProducerPayoutSerializer(DynamicModelSerializer):
    description_fields = _ProducerPayoutDescriptionFieldSerializer(many=True)
    beats_sold = SerializerMethodField()
    
    @staticmethod
    def get_beats_sold(producer_payout: ProducerPayout):
        try:
            previous_payout_date = ProducerPayout.objects.filter(producer=producer_payout.producer,
                                                                 date__lt=producer_payout.date).latest('date').date
            return OrderItem.objects.filter(beat__beatproducerrelation__producer=producer_payout.producer,
                                            order__date__gt=previous_payout_date,
                                            order__status=Order.STATUS_COMPLETE).count()
        except ProducerPayout.DoesNotExist:
            # first payout, so we get all sold beats
            return OrderItem.objects.filter(beat__beatproducerrelation__producer=producer_payout.producer,
                                            order__status=Order.STATUS_COMPLETE).count()
    
    @staticmethod
    def _update_description_fields(instance: ProducerPayout, description_fields: List[dict]):
        # delete old description fields
        instance.description_fields.all().delete()
        # create new ones
        for x in description_fields:
            ProducerPayoutDescriptionField.objects.create(producer_payout=instance, **x)
    
    def create(self, validated_data):
        description_fields: List[dict] = validated_data.pop('description_fields')
        instance: ProducerPayout = super().create(validated_data)
        self._update_description_fields(instance, description_fields)
        return instance
    
    def update(self, instance, validated_data):
        description_fields: List[dict] = validated_data.pop('description_fields')
        instance: ProducerPayout = super().update(instance, validated_data)
        self._update_description_fields(instance, description_fields)
        return instance
    
    class Meta:
        model = ProducerPayout
        fields = ProducerPayout.public_fields
