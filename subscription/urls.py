from django.urls import path
from subscription.views import SubscriptionHistory


urlpatterns = [
    path('history/', SubscriptionHistory.as_view(), name='history'),
]