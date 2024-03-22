from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SeeTaskListView(generics.ListAPIView):
    attribute = None
