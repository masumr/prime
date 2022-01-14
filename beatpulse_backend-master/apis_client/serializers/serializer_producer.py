from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import SerializerMethodField

from apis_client.mixins.mixin_producer import MixinProducerSerializer
from models.models import Producer


class ProducerSerializer(DynamicModelSerializer, MixinProducerSerializer):
    # they should in the mixin
    number_of_followers = SerializerMethodField()
    number_of_beats = SerializerMethodField()
    
    class Meta:
        model = Producer
        fields = Producer.public_fields
