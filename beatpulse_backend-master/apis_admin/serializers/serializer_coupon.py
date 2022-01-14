from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from models.models import Coupon, LicenseOption


class _LicenseOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseOption
        fields = ('id', 'name')


class CouponSerializer(DynamicModelSerializer):
    licenses = _LicenseOptionSerializer(many=True, read_only=True)
    licenses_ids = serializers.PrimaryKeyRelatedField(queryset=LicenseOption.objects.all(), source='licenses',
                                                      many=True, write_only=True)
    
    class Meta:
        model = Coupon
        fields = Coupon.public_fields + ('licenses_ids',)
