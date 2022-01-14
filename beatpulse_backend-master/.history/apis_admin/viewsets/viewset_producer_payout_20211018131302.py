from apis_admin.permissions.permissions import IsAdminOrIsProducerAndReadOnly
from apis_admin.serializers.serializer_producer_payout import ProducerPayoutSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import ProducerPayout, Profile, Producer


class ProducerPayoutViewSet(AdminDynamicModelViewset):
    queryset = ProducerPayout.objects.order_by('-id')
    serializer_class = ProducerPayoutSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    permission_classes = (IsAdminOrIsProducerAndReadOnly,)
    
    def get_queryset(self, **kwargs):
        # if is a producer
        try:
            producer: Producer = self.request.user.producer
            return self.queryset.filter(producer=producer)
        # else if is an admin
        except Producer.DoesNotExist:
            return super(ProducerPayoutViewSet, self).get_queryset()
