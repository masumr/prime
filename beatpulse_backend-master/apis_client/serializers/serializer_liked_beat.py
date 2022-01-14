from dynamic_rest.serializers import DynamicModelSerializer

from models.models import LikedBeat


class LikedBeatSerializer(DynamicModelSerializer):
    class Meta:
        model = LikedBeat
        fields = ('beat',)
