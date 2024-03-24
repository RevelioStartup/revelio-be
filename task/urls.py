from django.urls import path
from .views import (
    TaskCreateView,
    SeeTaskListView,
    TaskDetailView,
)

urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-create'),
    path('<uuid:event_id>/', SeeTaskListView.as_view(), name='get-task-list'),
    path('<uuid:event_id>/<int:task_id>/', TaskDetailView.as_view(), name='detail-task'),
]