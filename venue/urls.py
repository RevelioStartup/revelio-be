from django.urls import path
from .views import (
    VenueEventListView,
    VenueListCreateView,
    VenueRetrieveUpdateDestroyView,
    PhotoCreateView,
    PhotoRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('venues/', VenueListCreateView.as_view(), name='venue-list-create'),
    path('venues/<int:pk>/', VenueRetrieveUpdateDestroyView.as_view(), name='venue-retrieve-update-destroy'),
    path('venues/event/<int:event_id>/', VenueEventListView.as_view(), name='venue-event-list'),
    path('photos/', PhotoCreateView.as_view(), name='photo-create'),
    path('photos/<int:pk>/', PhotoRetrieveUpdateDestroyView.as_view(), name='photo-retrieve-update-destroy'),
]
