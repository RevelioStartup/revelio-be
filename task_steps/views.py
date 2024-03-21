from rest_framework import generics
from .models import TaskStep
from .serializers import TaskStepSerializer


class TaskStepListCreateView(generics.ListCreateAPIView):
    queryset = TaskStep.objects.all()
    serializer_class = TaskStepSerializer
