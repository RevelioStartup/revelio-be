from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from event.models import Event
from task_steps.models import TaskStep
from subscription.models import Subscription

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsTaskStepOwner(BasePermission):
    """
    Custom permission to only allow owners of an event to edit it.
    """
    def has_permission(self, request, view):
        if hasattr(request, 'data'):
            task_step_id = request.data.get('task_step')

        if not task_step_id:
            raise ValidationError('No task step ID provided.')

        try:
            task_step = TaskStep.objects.get(id=task_step_id)
            return task_step.user == request.user
        except TaskStep.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.event.user == request.user
class IsEventOwner(BasePermission):
    """
    Custom permission to only allow owners of an event to edit it.
    """
    def has_permission(self, request, view):
        event_id = view.kwargs.get('event_id')

        if not event_id and hasattr(request, 'data'):
            event_id = request.data.get('event')

        if not event_id:
            raise ValidationError('No event ID provided.')

        try:
            event = Event.objects.get(id=event_id)
            return event.user == request.user
        except Event.DoesNotExist:
            return False


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