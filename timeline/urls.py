from django.urls import path
from .views import (
    TimelineCreateView
)

urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
]