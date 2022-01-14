from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from apis_client.mixins.mixin_trending_beat import MixinTrendingBeatSerializer
from apis_client.serializers.serializer_beat import BeatSerializer


class TrendingBeatSerializer(DynamicModelSerializer, MixinTrendingBeatSerializer):
    beat = DynamicRelationField(BeatSerializer, embed=True)
