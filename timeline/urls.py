from django.urls import path
from .views import (
    TimelineCreateView,
    TimelineDeleteView,
    TimelineList,
)

urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
    path('<uuid:id>/delete/', TimelineDeleteView.as_view(), name='timeline-delete'),
    path('<uuid:event_id>/', TimelineList.as_view(), name='event-timelines'),

]