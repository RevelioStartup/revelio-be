from django.urls import path
from .views import (
    TaskStepCreateListView,
    TaskStepDestroyView,
    DeleteAllTaskStepsView,
)

urlpatterns = [
    path('', TaskStepCreateListView.as_view(), name='task-step-create'),
    path('<uuid:pk>/', TaskStepDestroyView.as_view(), name='task-step-detail'),
    path('tasks/<int:task_id>/delete-all-steps/', DeleteAllTaskStepsView.as_view(), name='delete-all-task-steps'),
]
