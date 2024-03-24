from rest_framework import generics

from utils.permissions import IsOwner
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
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwner]
    def get_queryset(self):
        return Task.objects.filter(event_id=self.kwargs['event_id'])
    def patch(self, request, *args, **kwargs):
        return NotImplementedError('Patch Method has not been implemented yet')