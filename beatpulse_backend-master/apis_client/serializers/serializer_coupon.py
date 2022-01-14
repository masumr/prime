from dynamic_rest.serializers import DynamicModelSerializer

from models.models import Coupon


class CouponSerializer(DynamicModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
