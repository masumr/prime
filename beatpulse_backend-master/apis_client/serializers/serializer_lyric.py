from dynamic_rest.serializers import DynamicModelSerializer

from models.models import Lyric


class LyricSerializer(DynamicModelSerializer):
    # beat = BeatSerializer(read_only=True, embed=True)
    # beat_id = serializers.PrimaryKeyRelatedField(queryset=Beat.objects.all(), source='beat', write_only=True)
    
    class Meta:
        model = Lyric
        fields = Lyric.public_fields + ('beat',)
        # deferred_fields = ('beat',)
