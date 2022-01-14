from apis_client.serializers.serializer_beat_key import BeatKeySerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import BeatKey


class BeatKeyViewSet(ReadOnlyDynamicModelViewset):
    queryset = BeatKey.objects.order_by('name')
    serializer_class = BeatKeySerializer
