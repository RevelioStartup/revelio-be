from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.owner == request.user

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user