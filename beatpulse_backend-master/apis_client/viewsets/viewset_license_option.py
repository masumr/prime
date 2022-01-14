from apis_client.serializers.serializer_license_option import LicenseOptionSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import LicenseOption


class LicenseOptionViewSet(ReadOnlyDynamicModelViewset):
    queryset = LicenseOption.objects.order_by('price')
    serializer_class = LicenseOptionSerializer
