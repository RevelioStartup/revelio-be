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
    
class IsPremiumUser(BasePermission):
    """
    Permission to check whether the current user is a premium user (subscribed right now)
    """
    def has_permission(self, request, view):
        user = request.user
        
        subscriptions = Subscription.objects.filter(user = user)
        
        is_active_subscriptions = [True for subscription in subscriptions if subscription.is_active]
        
        return len(is_active_subscriptions) > 0
    
def get_current_subscription(user):
    subscriptions = Subscription.objects.filter(user = user).order_by('-start_date')
    is_active_subscriptions = [subscription for subscription in subscriptions if subscription.is_active]
    
    return is_active_subscriptions[0] if len(is_active_subscriptions) > 0 else None
class HasEventPlanner(BasePermission):
    """
    Permission to check whether the current user can access event planner
    """
    
    def has_permission(self, request, view):
        user = request.user
        current_subscription = get_current_subscription(user)
        
        if current_subscription:
            return current_subscription.plan.event_planner
        
        return False
    
class HasEventTracker(BasePermission):
    """
    Permission to check whether the current user can access event tracker
    """
    
    def has_permission(self, request, view):
        user = request.user
        current_subscription = get_current_subscription(user)
        
        if current_subscription:
            return current_subscription.plan.event_tracker
        return False
    
class HasEventTimeline(BasePermission):
    """
    Permission to check whether the current user can access event timeline
    """
    
    def has_permission(self, request, view):
        user = request.user
        current_subscription = get_current_subscription(user)
        
        if current_subscription:
            return current_subscription.plan.event_timeline
        return False
    
class HasEventRundown(BasePermission):
    """
    Permission to check whether the current user can access event rundown
    """
    
    def has_permission(self, request, view):
        user = request.user
        current_subscription = get_current_subscription(user)
        
        if current_subscription:
            return current_subscription.plan.event_rundown
        return False

class HasAIAssistant(BasePermission):
    """
    Permission to check whether the current user can access AI assistant
    """
    
    def has_permission(self, request, view):
        user = request.user
        current_subscription = get_current_subscription(user)
        
        if current_subscription:
            return current_subscription.plan.ai_assistant
        return False