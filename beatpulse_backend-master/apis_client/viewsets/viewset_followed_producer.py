from apis_client.serializers.serializer_followed_producer import FollowedProducerSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import FollowedProducer


class FollowedProducerViewSet(ReadOnlyDynamicModelViewset):
    queryset = FollowedProducer.objects.all()
    serializer_class = FollowedProducerSerializer
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self, **kwargs):
        return self.queryset.filter(profile=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)
