from apis_admin.serializers.serializer_license_option import LicenseOptionSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import LicenseOption


class LicenseOptionViewSet(AdminDynamicModelViewset):
    queryset = LicenseOption.objects.order_by('price')
    serializer_class = LicenseOptionSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
