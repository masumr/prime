from dynamic_rest.viewsets import DynamicModelViewSet

from apis_client.serializers.serializer_billing_info import BillingInfoSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import BillingInfo


class BillingInfoViewSet(ReadOnlyDynamicModelViewset):
    queryset = BillingInfo.objects.all()
    serializer_class = BillingInfoSerializer
    http_method_names = ['get', 'patch']
    
    def get_queryset(self, **kwargs):
        return self.queryset.filter(profile=self.request.user)
