from rest_framework.permissions import BasePermission, SAFE_METHODS

from models.models import Producer


class IsDashboardUser(BasePermission):
    """
    User belongs to a group
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.groups.count() > 0


class CanUpload(BasePermission):
    """
    User belongs to a group
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.can_upload_in_dashboard()


class IsAdminOrUploader(CanUpload):
    pass


class IsAdminOrUploaderOrIsProducerAndReadOnly(BasePermission):
    """
    The request is a read-only request and is made by a Producer
    or is made by an admin
    """
    
    def has_permission(self, request, view):
        if request.user is None:
            return False
        
        if request.user.can_upload_in_dashboard():
            return True
        
        # check if it is a producer
        # if it is not it will raise an error
        try:
            can_make_request = request.user.producer is not None and request.method in SAFE_METHODS
            return can_make_request
        except Producer.DoesNotExist:
            return False


class IsAdminOrIsProducerAndReadOnly(BasePermission):
    """
    The request is a read-only request and is made by a Producer
    or is made by an admin
    """
    
    def has_permission(self, request, view):
        if request.user is None:
            return False
        
        if request.user.is_admin():
            return True
        
        try:
            can_make_request = request.user.producer is not None and request.method in SAFE_METHODS
            return can_make_request
        except Producer.DoesNotExist:
            return False


class IsAdminOrIsProducer(BasePermission):
    """
    The request is  made by a Producer or is made by an admin
    """
    
    def has_permission(self, request, view):
        if request.user is None:
            return False
        
        if request.user.is_admin():
            return True
        
        try:
            is_producer = request.user.producer is not None
            return is_producer
        except Producer.DoesNotExist:
            return False


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    
    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS or
                request.user and
                request.user.is_admin()
        )
