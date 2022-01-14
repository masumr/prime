from dynamic_rest.serializers import DynamicModelSerializer

from models.models import BeatKey


class BeatKeySerializer(DynamicModelSerializer):
    class Meta:
        model = BeatKey
        fields = '__all__'
