from rest_framework import generics

from utils.permissions import IsEventOwner, IsOwner
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

class UpdateTaskView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsEventOwner]
    lookup_url_kwarg = 'task_id'
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(event_id=self.kwargs['event_id'], id=self.kwargs['task_id'])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)