from rest_framework.permissions import BasePermission

import subscription
from subscription.models import Subscription

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
    
class isPremiumUser(BasePermission):
    """
    Permission to check whether the current user is a premium user (subscribed right now)
    """
    def has_permission(self, request, view):
        user = request.user
        
        subscriptions = Subscription.objects.filter(user = user)
        
        is_active_subscriptions = [True for subscription in subscriptions if subscription.is_active]
        
        return len(is_active_subscriptions) > 0