from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveDestroyAPIView

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SeeTaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'event_id'
    permission_classes = [IsAuthenticated]
