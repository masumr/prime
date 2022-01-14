from apis_client.serializers.serializer_own_profile import OwnProfileSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Profile


class OwnProfileViewSet(ReadOnlyDynamicModelViewset):
    queryset = Profile.objects.all()
    serializer_class = OwnProfileSerializer
    http_method_names = ['get', 'patch']
    
    def get_queryset(self, **kwargs):
        return self.queryset.filter(pk=self.request.user.id)
