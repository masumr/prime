from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from models.models import LicenseOption, LicenseOptionDescriptionField


class LicenseOptionDescriptionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseOptionDescriptionField
        fields = ('id', 'description', 'is_included')


class LicenseOptionSerializer(DynamicModelSerializer):
    description_fields = LicenseOptionDescriptionFieldSerializer(many=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["description_fields"] = sorted(response["description_fields"], key=lambda x: x["id"])
        return response
    
    class Meta:
        model = LicenseOption
        fields = LicenseOption.public_fields
