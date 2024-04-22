from django.urls import path
from .views import (
    TimelineCreateView,
    TimelineDeleteView,
    TimelineDetailView
)

urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
    path('<uuid:id>/', TimelineDetailView.as_view(), name='timeline-detail'),
    path('<uuid:id>/delete/', TimelineDeleteView.as_view(), name='timeline-delete'),
    path('create/', TimelineCreateView.as_view(), name='timeline-create'),
]