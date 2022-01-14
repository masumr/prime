from django.db.models import Count

from apis_admin.permissions.permissions import IsAdminOrIsProducer
from apis_admin.serializers.serializer_producer import ProducerSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import Producer


class ProducerViewSet(AdminDynamicModelViewset):
    queryset = Producer.objects.annotate(beat_count=Count('beat'))
    serializer_class = ProducerSerializer
    http_method_names = ['get', 'patch']
    permission_classes = (IsAdminOrIsProducer,)
    
    def get_queryset(self, **kwargs):
        # if is a producer
        try:
            producer: Producer = self.request.user.producer
            return self.queryset.filter(pk=producer.pk)
        # else if is an admin
        except Producer.DoesNotExist:
            return super(ProducerViewSet, self).get_queryset()
