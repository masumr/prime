from apis_client.serializers.serializer_deal import DealSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Deal


class DealViewSet(ReadOnlyDynamicModelViewset):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
