from apis_admin.serializers.serializer_deal import DealSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import Deal


class DealViewSet(AdminDynamicModelViewset):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
