from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from apis_admin.serializers.serializer_profile import ProfileSerializer
from models.models import Profile


class ProfileViewSet(AdminDynamicModelViewset):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'delete']
