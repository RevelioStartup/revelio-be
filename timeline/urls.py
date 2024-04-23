from django.urls import path
from .views import (
    TimelineCreateView,
    TimelineDetailView
)

urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
    path('<uuid:pk>/', TimelineDetailView.as_view(), name='timeline-detail'),
]