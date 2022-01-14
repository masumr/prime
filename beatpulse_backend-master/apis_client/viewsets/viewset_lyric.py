from django.shortcuts import get_object_or_404
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework import status
from rest_framework.response import Response

from apis_client.serializers.serializer_lyric import LyricSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import Lyric


class LyricViewSet(ReadOnlyDynamicModelViewset):
    queryset = Lyric.objects.all()
    serializer_class = LyricSerializer
    # patch and delete are safe because the queryset hides stuff that are not of the user
    http_method_names = ['get', 'patch', 'post', 'delete']
    
    def get_queryset(self, **kwargs):
        return self.queryset.filter(profile=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        lyric = get_object_or_404(Lyric, beat_id=kwargs['pk'], profile=request.user)
        lyric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
