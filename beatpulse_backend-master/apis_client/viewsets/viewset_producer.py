from django.db.models import Count

from apis_client.serializers.serializer_producer import ProducerSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Producer


class ProducerViewSet(ReadOnlyDynamicModelViewset):
    queryset = Producer.objects.annotate(beat_count=Count('beat')).filter(beat_count__gte=0)
    serializer_class = ProducerSerializer
