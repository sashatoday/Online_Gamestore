from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdminElseReadOnly(BasePermission):
    """
    Custom permission to only allow owners or admin of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed to the admin
        if request.user.is_staff == True:
            return True
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'developer'):
            return obj.developer.user == request.user
