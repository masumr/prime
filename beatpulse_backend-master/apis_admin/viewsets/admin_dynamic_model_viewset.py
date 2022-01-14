from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.permissions import IsAdminUser


class AdminDynamicModelViewset(DynamicModelViewSet):
    http_method_names = ['get']
    permission_classes = (IsAdminUser,)
