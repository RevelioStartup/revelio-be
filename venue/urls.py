from django.urls import path
from .views import (
    VenueEventListView,
    VenueListCreateView,
    VenueRetrieveUpdateDestroyView,
    PhotoCreateView,
    PhotoRetrieveUpdateDestroyView,
    VenueStatusUpdateAPIView
)

urlpatterns = [
    path('', VenueListCreateView.as_view(), name='venue-list-create'),
    path('<int:pk>/', VenueRetrieveUpdateDestroyView.as_view(), name='venue-retrieve-update-destroy'),
    path('<int:pk>/status/', VenueStatusUpdateAPIView.as_view(), name='venue-status-update'),
    path('event/<int:event_id>/', VenueEventListView.as_view(), name='venue-event-list'),
    path('photos/', PhotoCreateView.as_view(), name='photo-venue-create'),
    path('photos/<int:pk>/', PhotoRetrieveUpdateDestroyView.as_view(), name='photo-venue-retrieve-update-destroy'),
]
