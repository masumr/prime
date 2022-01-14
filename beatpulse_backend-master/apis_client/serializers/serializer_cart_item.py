from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from apis_client.serializers.serializer_beat import BeatSerializer
from apis_client.serializers.serializer_license_option import LicenseOptionSerializer
from models.models import CartItem, Beat, LicenseOption


class CartItemSerializer(DynamicModelSerializer):
    beat = DynamicRelationField(BeatSerializer, embed=True, read_only=True)
    beat_id = serializers.PrimaryKeyRelatedField(
        queryset=Beat.objects.all(), source='beat', write_only=True)
    
    license_option = DynamicRelationField(LicenseOptionSerializer, embed=True, read_only=True)
    license_option_id = serializers.PrimaryKeyRelatedField(
        queryset=LicenseOption.objects.all(), source='license_option', write_only=True)
    
    class Meta:
        model = CartItem
        fields = ('id', 'beat', 'beat_id', 'license_option', 'license_option_id')
