from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from apis_admin.serializers.serializer_beat import BeatSerializer
from apis_client.mixins.mixin_trending_beat import MixinTrendingBeatSerializer


class TrendingBeatSerializer(DynamicModelSerializer, MixinTrendingBeatSerializer):
    beat = DynamicRelationField(BeatSerializer, embed=True)
