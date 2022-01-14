from apis_client.mixins.mixin_beat_group import MixinGenreViewSet, MixinMoodViewSet
from apis_client.serializers.serializers_beat_groups import PlaylistSerializer, MoodSerializer, GenreSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Playlist


class PlaylistViewSet(ReadOnlyDynamicModelViewset):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class GenreViewSet(ReadOnlyDynamicModelViewset, MixinGenreViewSet):
    serializer_class = GenreSerializer


class MoodViewSet(ReadOnlyDynamicModelViewset, MixinMoodViewSet):
    serializer_class = MoodSerializer
