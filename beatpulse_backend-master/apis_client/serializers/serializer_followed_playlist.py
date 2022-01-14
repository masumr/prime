from dynamic_rest.serializers import DynamicModelSerializer

from models.models import FollowedPlaylist


class FollowedPlaylistSerializer(DynamicModelSerializer):
    class Meta:
        model = FollowedPlaylist
        fields = ('id', 'playlist')
