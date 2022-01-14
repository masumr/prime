from django.db.models import Count

from apis_admin.permissions.permissions import IsAdminOrUploader
from apis_admin.serializers.serializers_beat_groups import PlaylistSerializer, MoodSerializer, GenreSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from apis_client.mixins.mixin_beat_group import MixinGenreViewSet, MixinMoodViewSet
from models.models import Playlist


class PlaylistViewSet(AdminDynamicModelViewset):
    queryset = Playlist.objects.annotate(number_of_followers=Count('followedplaylist')).order_by('-id')
    serializer_class = PlaylistSerializer
    permission_classes = (IsAdminOrUploader,)
    http_method_names = ['get', 'patch', 'post', 'delete']


class GenreViewSet(AdminDynamicModelViewset, MixinGenreViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrUploader,)
    http_method_names = ['get', 'patch', 'post', 'delete']


class MoodViewSet(AdminDynamicModelViewset, MixinMoodViewSet):
    serializer_class = MoodSerializer
    permission_classes = (IsAdminOrUploader,)
    http_method_names = ['get', 'patch', 'post', 'delete']
