from django.urls import path
from .views import (
    TimelineCreateView,
    TimelineDetailView,
    TimelineDeleteView,
    TimelineList,
)

urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
    path('<uuid:pk>/', TimelineDetailView.as_view(), name='timeline-detail'),
    path('<uuid:id>/delete/', TimelineDeleteView.as_view(), name='timeline-delete'),
    path('<uuid:event_id>/view', TimelineList.as_view(), name='event-timelines'),
]