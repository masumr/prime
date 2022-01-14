from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from models.models import Deal, LicenseOption


class _LicenseOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseOption
        fields = ('id', 'name')


class DealSerializer(DynamicModelSerializer):
    excluded_licenses = _LicenseOptionSerializer(many=True, read_only=True)
    excluded_licenses_ids = serializers.PrimaryKeyRelatedField(queryset=LicenseOption.objects.all(), source='excluded_licenses',
                                                      many=True, write_only=True)

    class Meta:
        model = Deal
        fields = Deal.public_fields + ('excluded_licenses_ids',)
