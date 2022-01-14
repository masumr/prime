from django.db.models import Q
from django.utils import timezone

from apis_client.serializers.serializer_coupon import CouponSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Coupon


class CouponViewSet(ReadOnlyDynamicModelViewset):
    queryset = Coupon.objects.filter(Q(expiration_date__gte=timezone.now()) | Q(expiration_date__isnull=True))
    serializer_class = CouponSerializer
