from django.urls import path
from .views import (
    TaskCreateView,
    SeeTaskListView,
    UpdateTaskView
)

urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-create'),
    path('<uuid:event_id>/', SeeTaskListView.as_view(), name='get-task-list'),
    path('<uuid:event_id>/<int:task_id>/', UpdateTaskView.as_view(), name='update-task'),
]