from dynamic_rest.serializers import DynamicModelSerializer

from models.models import BillingInfo


class BillingInfoSerializer(DynamicModelSerializer):
    class Meta:
        model = BillingInfo
        fields = BillingInfo.public_fields
        read_only_fields = BillingInfo.read_only_fields
