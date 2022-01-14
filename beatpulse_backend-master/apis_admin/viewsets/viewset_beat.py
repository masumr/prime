from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response

from apis_admin.permissions.permissions import IsAdminOrUploaderOrIsProducerAndReadOnly
from apis_admin.serializers.serializer_beat import BeatSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from models.models import Beat, Producer


class BeatViewSet(AdminDynamicModelViewset):
    queryset = Beat.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BeatSerializer
    permission_classes = (IsAdminOrUploaderOrIsProducerAndReadOnly,)
    http_method_names = ['get', 'patch', 'post', 'delete']
    
    @login_required
    def get_queryset(self, **kwargs):
        # if is a producer
        try:
            producer: Producer = self.request.user.producer
            return self.queryset.filter(producers=producer)
        # else if is an admin
        except Producer.DoesNotExist:
            return super(BeatViewSet, self).get_queryset()
    
    def destroy(self, request, *args, **kwargs):
        instance: Beat = self.get_object()
        # we don't really delete, but we hide them
        instance.is_deleted = True
        instance.is_published = False
        
        # delete related items
        instance.cartitem_set.all().delete()
        instance.likedbeat_set.all().delete()
        instance.trendingbeat_set.all().delete()
        instance.lyric_set.all().delete()
        
        instance.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
