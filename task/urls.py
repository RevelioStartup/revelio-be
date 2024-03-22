from django.urls import path
from .views import (
    TaskCreateView,
    SeeTaskListView
)

urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-create'),
    path('<uuid:event_id>/', SeeTaskListView.as_view(), name='get-task-list'),
]