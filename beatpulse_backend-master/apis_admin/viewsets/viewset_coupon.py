from apis_admin.serializers.serializer_coupon import CouponSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import Coupon


class CouponViewSet(AdminDynamicModelViewset):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
