from typing import List

from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from models.models import LicenseOption, LicenseOptionDescriptionField


class LicenseOptionDescriptionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseOptionDescriptionField
        fields = ('id', 'description', 'is_included')


class LicenseOptionSerializer(DynamicModelSerializer):
    description_fields = LicenseOptionDescriptionFieldSerializer(many=True)
    
    @staticmethod
    def _update_description_fields(instance: LicenseOption, description_fields: List[dict]):
        # delete old description fields
        instance.description_fields.all().delete()
        # create new ones
        for x in description_fields:
            LicenseOptionDescriptionField.objects.create(license_option=instance, **x)
    
    def create(self, validated_data):
        description_fields: List[dict] = validated_data.pop('description_fields')
        instance: LicenseOption = super().create(validated_data)
        self._update_description_fields(instance, description_fields)
        return instance
    
    def update(self, instance, validated_data):
        description_fields: List[dict] = validated_data.pop('description_fields')
        instance: LicenseOption = super().update(instance, validated_data)
        self._update_description_fields(instance, description_fields)
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["description_fields"] = sorted(response["description_fields"], key=lambda x: x["id"])
        return response
    
    class Meta:
        model = LicenseOption
        fields = LicenseOption.public_fields
