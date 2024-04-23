from django.urls import path
from .views import (
    TimelineCreateView,
    TimelineDeleteView,
)

urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
    path('<uuid:id>/delete/', TimelineDeleteView.as_view(), name='timeline-delete'),
]