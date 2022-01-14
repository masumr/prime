from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

from apis_client.serializers.serializer_cart_item import CartItemSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import CartItem


class CartItemViewSet(ReadOnlyDynamicModelViewset):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'delete']
    
    @login_required
    def get_queryset(self, **kwargs):
        return self.queryset.filter(profile=self.request.user)
    
    @login_required
    def perform_create(self, serializer):
        # delete an eventually already present cart item of the same beat
        CartItem.objects.filter(profile=self.request.user, beat_id=self.request.data['beat_id']).delete()
        serializer.save(profile=self.request.user)
