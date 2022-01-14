from django.contrib.auth.decorators import login_required
from apis_admin.permissions.permissions import IsDashboardUser
from apis_admin.serializers.serializer_own_profile import OwnProfileSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import Profile


class OwnProfileViewSet(AdminDynamicModelViewset):
    queryset = Profile.objects.all()
    serializer_class = OwnProfileSerializer
    http_method_names = ['get', 'patch']
    permission_classes = (IsDashboardUser,)
    
    @login_required
    def get_queryset(self, **kwargs):
        return self.queryset.filter(pk=self.request.user.id)
