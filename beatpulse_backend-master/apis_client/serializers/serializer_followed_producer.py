from dynamic_rest.serializers import DynamicModelSerializer

from models.models import FollowedProducer


class FollowedProducerSerializer(DynamicModelSerializer):
    class Meta:
        model = FollowedProducer
        fields = ('id', 'producer')
