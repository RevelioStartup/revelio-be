from django.urls import path
from .views import (
    VendorEventListView,
    VendorListCreateView,
    VendorRetrieveUpdateDestroyView,
    PhotoCreateView,
    PhotoRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'),
    path('event/<int:event_id>/', VendorEventListView.as_view(), name='vendor-event-list'),
    path('photos/', PhotoCreateView.as_view(), name='photo-create'),
    path('photos/<int:pk>/', PhotoRetrieveUpdateDestroyView.as_view(), name='photo-retrieve-update-destroy'),
]
