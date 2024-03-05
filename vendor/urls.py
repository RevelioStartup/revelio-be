from django.urls import path
from .views import (
    VendorEventListView,
    VendorListCreateView,
    VendorRetrieveUpdateDestroyView,
    PhotoCreateView,
    PhotoRetrieveUpdateDestroyView,
    VendorStatusUpdateAPIView
)

urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'),
    path('event/<int:event_id>/', VendorEventListView.as_view(), name='vendor-event-list'),
      path('<int:pk>/status/', VendorStatusUpdateAPIView.as_view(), name='vendor-status-update'),
    path('photos/', PhotoCreateView.as_view(), name='photo-create'),
    path('photos/<int:pk>/', PhotoRetrieveUpdateDestroyView.as_view(), name='photo-retrieve-update-destroy'),
]
