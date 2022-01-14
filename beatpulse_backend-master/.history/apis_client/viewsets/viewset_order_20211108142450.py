from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

from apis_client.serializers.serializer_order import OrderSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Order


class OrderViewSet(ReadOnlyDynamicModelViewset):
    queryset = Order.objects.order_by('-id').filter(status=Order.STATUS_COMPLETE)
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    
    @login_required
    def get_queryset(self, **kwargs):
        return self.queryset.filter(profile=self.request.user)
