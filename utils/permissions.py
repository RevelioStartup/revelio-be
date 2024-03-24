from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsEventOwner(BasePermission):
    """
    Custom permission to only allow owners of an event to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.event.user == request.user