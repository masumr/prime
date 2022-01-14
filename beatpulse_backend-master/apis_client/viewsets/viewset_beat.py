from apis_client.serializers.serializer_beat import BeatSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Beat


class BeatViewSet(ReadOnlyDynamicModelViewset):
    queryset = Beat.objects.filter(is_published=True)
    serializer_class = BeatSerializer
