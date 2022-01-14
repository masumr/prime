from dynamic_rest.serializers import DynamicModelSerializer

from models.models import Deal


class DealSerializer(DynamicModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'
