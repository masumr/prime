from django.db.models import Sum
from django.utils.text import slugify
from dynamic_rest.fields import SerializerMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from analytics_module.models import BeatPlay
from apis_client.mixins.mixin_producer import MixinProducerSerializer
from models.models import Producer, ProducerPayout, OrderItem, Order


class ProducerSerializer(DynamicModelSerializer, MixinProducerSerializer):
    full_name = serializers.CharField(source='profile.first_name')
    beats_sold = SerializerMethodField()
    total_sales = SerializerMethodField()
    total_payouts = SerializerMethodField()
    last_payment = SerializerMethodField()
    # they should in the mixin
    number_of_followers = SerializerMethodField()
    number_of_beats = SerializerMethodField()
    number_of_beat_plays = SerializerMethodField()
    
    @staticmethod
    def get_beats_sold(producer: Producer):
        return OrderItem.objects.filter(order__status=Order.STATUS_COMPLETE,
                                        beat__beatproducerrelation__producer=producer).count()
    
    @staticmethod
    def get_total_sales(producer: Producer):
        return producer.get_total_sales()
    
    @staticmethod
    def get_total_payouts(producer: Producer):
        return ProducerPayout.objects.filter(producer=producer).aggregate(Sum('payed_amount'))['payed_amount__sum']
    
    @staticmethod
    def get_last_payment(producer: Producer):
        try:
            return ProducerPayout.objects.filter(producer=producer).latest('date').date
        except ProducerPayout.DoesNotExist:
            return None
    
    @staticmethod
    def get_number_of_beat_plays(producer: Producer):
        return BeatPlay.objects.filter(beat__producers=producer).count()
    
    @staticmethod
    def _update_full_name(instance: Producer, full_name: str):
        instance.profile.first_name = full_name
        # instance.save()
    
    @staticmethod
    def _slugify(instance: Producer):
        instance.slug = slugify(instance.display_name)
    
    def create(self, validated_data):
        full_name: str = validated_data.pop('profile', {}).get('first_name')
        instance: Producer = super().create(validated_data)
        self._update_full_name(instance, full_name)
        self._slugify(instance)
        return instance
    
    def update(self, instance, validated_data):
        full_name: str = validated_data.pop('profile', {}).get('first_name')
        instance: Producer = super().update(instance, validated_data)
        self._update_full_name(instance, full_name)
        self._slugify(instance)
        return instance
    
    class Meta:
        model = Producer
        fields = Producer.public_fields + (
            'commission', 'date_of_creation', 'full_name', 'paypal_email', 'address', 'beats_sold', 'total_sales',
            'total_payouts', 'last_payment', 'image_logo_file_path', 'image_background_file_path',
            'number_of_beat_plays')
        read_only_fields = ('profile',)
        deferred_fields = (
            'number_of_followers', 'number_of_beats', 'beats_sold', 'total_sales', 'total_payouts', 'last_payment',
            'number_of_beat_plays')
