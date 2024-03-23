from django.urls import path
from .views import (
    TaskStepListCreateView,
    TaskStepDestroyView,
    DeleteAllTaskStepsView
)

urlpatterns = [
    path('', TaskStepListCreateView.as_view(), name='task-step-list-create'),
    path('<uuid:pk>/', TaskStepDestroyView.as_view(), name='task-step-detail'),
    path('tasks/<int:task_id>/delete-all-steps/', DeleteAllTaskStepsView.as_view(), name='delete-all-task-steps'),
]
