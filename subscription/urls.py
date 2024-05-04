from django.urls import path
from subscription.views import LatestSubscription, SubscriptionHistory


urlpatterns = [
    path('history/', SubscriptionHistory.as_view(), name='history'),
    path("latest/", LatestSubscription.as_view(), name="latest")
]