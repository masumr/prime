from dynamic_rest.viewsets import DynamicModelViewSet


class ReadOnlyDynamicModelViewset(DynamicModelViewSet):
    http_method_names = ['get']
