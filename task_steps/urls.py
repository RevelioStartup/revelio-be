from django.urls import path
from .views import (
TaskStepListCreateView
)

urlpatterns = [
    path('', TaskStepListCreateView.as_view(), name='task-step-list-create'),
]
