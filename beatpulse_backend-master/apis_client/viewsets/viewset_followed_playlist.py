from apis_client.serializers.serializer_followed_playlist import FollowedPlaylistSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import FollowedPlaylist


class FollowedPlaylistViewSet(ReadOnlyDynamicModelViewset):
    queryset = FollowedPlaylist.objects.all()
    serializer_class = FollowedPlaylistSerializer
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self, **kwargs):
        return self.queryset.filter(profile=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)
