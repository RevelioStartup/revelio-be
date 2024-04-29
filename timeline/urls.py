from django.urls import path
from .views import (
    TimelineCreateView,
    TimelineDetailView,
    TimelineDeleteView,
)

urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
    path('<uuid:pk>/', TimelineDetailView.as_view(), name='timeline-detail'),
    path('<uuid:id>/delete/', TimelineDeleteView.as_view(), name='timeline-delete'),
]