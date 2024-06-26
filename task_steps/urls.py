from django.urls import path
from .views import (
    TaskStepUpdateView,
    TaskStepCreateListView,
    TaskStepDestroyView,
    DeleteAllTaskStepsView,
    TaskStepAppendView
)

urlpatterns = [
    path('', TaskStepCreateListView.as_view(), name='task-step-create'),
    path('<uuid:pk>/', TaskStepDestroyView.as_view(), name='task-step-detail'),
    path('<uuid:pk>/edit/', TaskStepUpdateView.as_view(), name='task-step-update'),
    path('tasks/<int:task_id>/append/', TaskStepAppendView.as_view(), name='append-task-step'),
    path('tasks/<int:task_id>/delete-all-steps/', DeleteAllTaskStepsView.as_view(), name='delete-all-task-steps'),
]
