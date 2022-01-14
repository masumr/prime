from rest_framework import permissions


# TODO
class SameProfilePermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # if task belongs to someone else that's not gud
        # but if request is easy, that's gud
        return request.method not in ['POST', 'PATCH', 'DELETE']  # \
        # or Workspace.objects.filter(pk=request.data.get('workspace_id'), admin=request.user.profile).exists()
