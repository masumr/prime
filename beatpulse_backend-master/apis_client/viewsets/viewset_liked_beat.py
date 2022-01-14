from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apis_client.serializers.serializer_liked_beat import LikedBeatSerializer
from apis_client.viewsets.read_only_dynamic_model_viewset import ReadOnlyDynamicModelViewset
from models.models import LikedBeat


class LikedBeatViewSet(ReadOnlyDynamicModelViewset):
    queryset = LikedBeat.objects.all()
    serializer_class = LikedBeatSerializer
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self, **kwargs):
        return self.queryset.filter(profile=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        liked_beat = get_object_or_404(LikedBeat, beat_id=kwargs['pk'], profile=request.user)
        liked_beat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
