from django.http import HttpResponseForbidden

from apis_admin.serializers.serializer_order import OrderSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import Order


class OrderViewSet(AdminDynamicModelViewset):
    queryset = Order.objects.order_by('-id').exclude(status=Order.STATUS_PENDING)
    serializer_class = OrderSerializer
    http_method_names = ['get', 'delete']
    
    def destroy(self, request, *args, **kwargs):
        instance: Order = self.get_object()
        
        if instance.status == Order.STATUS_COMPLETE:
            return HttpResponseForbidden('Could not delete completed order')
        else:
            return super(OrderViewSet, self).destroy(request, *args, **kwargs)
    
    # https://github.com/AltSchool/dynamic-rest/issues/253#issuecomment-436446965
    # def filter_queryset(self, queryset):
    #     queryset = super(OrderViewSet, self).filter_queryset(queryset)
    #     order_id = self.request.GET.get('filter{id}')
    #     profile_email = self.request.GET.get('filter{profile.email}')
    #     if order_id and profile_email:
    #         queryset.filter(Q(id=order_id) | Q(profile__email__icontains=profile_email))
    #     return queryset
